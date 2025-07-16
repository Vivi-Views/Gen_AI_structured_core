# === Imports === #
from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List
import threading
import time
import os
import glob

from logger_config import setup_logger
from path_files_selector import FileSelectorModule
from data_provider import receive_files  # simple function you’ll define later
from data_extractor import receive_files

# =======================XXX======================= #

# === Logger === #
logger = setup_logger("main")

# =======================XXX======================= #


# === FastAPI App === #
app = FastAPI()

# === CORS Middleware === #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================XXX======================= #

# 🧠 Global Map	                    Creates resolved_path_map = {} to store mappings of {filename → absolute path}
# 🧵 Background Thread	            Runs a parallel background thread using threading.Thread(..., daemon=True)
# 🔁 Scans Periodically	            Every 10 seconds, it scans the specified directory and all its subfolders recursively
# 🔍 Extracts Info	            For each file found, it extracts the filename only and stores the full absolute path as its value
# 📌 Purpose	                    Enables your main app to resolve file names to absolute paths later using resolved_path_map.get(filename)
# 📋 Example Entry	            'sample1.pdf': 'C:/Users/vivek/Desktop/client_data/sample1.pdf'
# 🪵 Logs Status	            Logs a message every 10 seconds confirming map is updated (or logs an error)
# 🛡️ Daemon Thread	            Runs in the background and auto-exits when FastAPI shuts down

# === In-Memory Absolute Path Map === #
resolved_path_map = {}

def local_path_collector_thread(search_directory="C:/Users/"):
    """
    Background thread that continuously scans files under a known root directory
    and stores their absolute paths keyed by filename.
    """
    while True:
        try:
            for filepath in glob.glob(f"{search_directory}/**/*.*", recursive=True):
                filename = os.path.basename(filepath)
                resolved_path_map[filename] = filepath
            logger.info("[BACKGROUND] File map updated.")
        except Exception as e:
            logger.error(f"[BACKGROUND] Error updating file map: {str(e)}")
        time.sleep(10)  # Refresh every 10 seconds

# Start the background thread
threading.Thread(target=local_path_collector_thread, daemon=True).start()

# =======================XXX======================= #

# 🔌 Endpoint	Defines a GET API route at / — the root of your FastAPI app
# 🩺 Health Check	Acts as a simple health check to confirm the backend server is running
# 🔁 No Input	Does not require any input or parameters
# 📤 Returns	Always returns a static JSON response: {"message": "Xiphold project is up and running !!!"}
# 🧪 Use Case	Can be tested via browser, Postman, or curl to verify the API is online
# 🚦 Best Practice	Common practice to include a root or /ping endpoint in APIs for monitoring

# === Root Check Endpoint === #
@app.get("/")
def read_root():
    return {"message": "Xiphold project is up and running !!!"}

# =======================XXX======================= #

# ✅ Accepts	        folder_path from the request body (as a plain string)
# 🔄 Resolves	        Converts it to a clean absolute path using os.path.abspath()
# 🔎 Validates	        Checks if the resolved folder actually exists using os.path.exists()
# 🪵 Logs	            Logs both success and error messages using the main logger
# 📤 Returns	        Returns a JSON response with "absolute_path" if valid, or "error" if not
# 🚫 Handles Error	    Catches exceptions and returns a general error message if something goes wrong

# === Optional Standalone Folder Resolver === #
@app.post("/resolve-folder-path/")
def resolve_folder_path(folder_path: str = Body(..., embed=True)):
    """
    Accepts a folder path (string) and returns its absolute path if valid.
    """
    try:
        # This is the main code trying to get the absolute path
        absolute_path = os.path.abspath(folder_path)

        if not os.path.exists(absolute_path):
            logger.warning(f"[PATH RESOLVER] Folder not found: {absolute_path}")
            return {"error": f"Folder not found: {absolute_path}"}

        logger.info(f"[PATH RESOLVER] Absolute folder path resolved: {absolute_path}")
        return {"absolute_path": absolute_path}

    except Exception as e:
        logger.error(f"[PATH RESOLVER] Exception occurred: {str(e)}")
        return {"error": "Failed to resolve folder path"}


# =======================XXX======================= #

# 🔌 Endpoint	Defines a POST API route at /select-files/
# 📥 Accepts	JSON body from the frontend: { "file_paths": ["sample1.pdf", ...] }
# 🧠 In-Memory Map	Looks up each filename in the resolved_path_map (built by background thread)
# 🔄 Resolves Paths	Builds a list of absolute paths using that map
# 📁 Extracts Info	Uses os.path.dirname(...) to get the common folder path from the first resolved file
# 📄 Extracts Names	Uses os.path.basename(...) to get clean file names from paths
# 🩺 Verifies Path	Calls the resolve_folder_path() function to validate the folder
# 📤 Sends to Logic	Sends the folder_path and file_list to receive_files() (the next stage of processing)
# 🔁 Returns	Returns a JSON response to the frontend with folder_path and files
# 🪵 Logs Everything	Logs key events for traceability

# === File Selection Endpoint === #
@app.post("/select-files/")
async def select_files_endpoint(request: Request):
    try:
        logger.info("                                                             ")
        logger.info("# ================= Started New Iteration ================= #")
        logger.info("                                                             ")
        logger.info("[MAIN] API called: /select-files/")

        body = await request.json()
        filenames_from_frontend: List[str] = body.get("file_paths", [])
        logger.info(f"[MAIN > select-files] Files received from frontend: {filenames_from_frontend}")
        logger.info("                                                             ")

        # ✅ Use in-memory absolute path map from background thread
        absolute_paths = [resolved_path_map.get(name, name) for name in filenames_from_frontend]
        logger.info(f"[MAIN] Resolved absolute paths: {absolute_paths}")

        selector = FileSelectorModule()
        folder_path, file_list = selector.process_selected_files(absolute_paths)

        # Strip and lookup each filename
        absolute_paths = [
        resolved_path_map.get(name.strip()) for name in filenames_from_frontend
        if resolved_path_map.get(name.strip())
        ]

        logger.info(f"[MAIN] Resolved absolute paths: {absolute_paths}")

        # ✅ Get only folder path from first file
        folder_path = os.path.dirname(absolute_paths[0]) if absolute_paths else ""
        file_list = [os.path.basename(p) for p in absolute_paths]

        # ✅ Also run the folder resolver logic immediately
        folder_resolution_result = resolve_folder_path(folder_path=folder_path)
        logger.info(f"[MAIN] Folder resolution result: {folder_resolution_result}")
        


        # ✅ Sending the file paths and file names to data provider
        receive_files(folder_path, file_list)

        # ✅ Sending the file pats and file names to web page
        return {
            "folder_path": folder_path,
            "files": file_list
        }


    except Exception as e:
        logger.error(f"coming from main.py : Error in /select-files/: {str(e)}")
        return {"error": "coming from main.py : Failed to process file selection"}