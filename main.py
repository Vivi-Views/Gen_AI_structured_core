# === Imports === #
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List

from logger_config import setup_logger
from path_files_selector import FileSelectorModule
from data_provider import receive_files  # simple function you’ll define later

# === Logger === #
logger = setup_logger("main")

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

# CORS is needed in main.py to allow your frontend (running on a different domain or port) to securely access the FastAPI backend APIs.


# === Root Check Endpoint === #
@app.get("/")
def read_root():
    return {"message": "Xiphold project is up and running !!!"}





# === File Selection Endpoint === #
@app.post("/select-files/")
async def select_files_endpoint(request: Request):
    try:
        logger.info("                                                             ")
        logger.info("# ================= Started New Iteration ================= #")
        logger.info("                                                             ")
        logger.info("[MAIN] API called: /select-files/")

        body = await request.json()
        files: List[str] = body.get("file_paths", [])
        logger.info(f"[MAIN] Files received from frontend: {files}")
        logger.info("                                                             ")

        # ✅ Running the path_files_selector > (FileSelectorModule)process_selected_files
        selector = FileSelectorModule() # class in path_files_selector module
        folder_path, file_list = selector.process_selected_files(files)

        # ✅ Send to data_provider
        receive_files(folder_path, file_list)

        return {
            "folder_path": folder_path,
            "files": file_list
        }

    except Exception as e:
        logger.error(f"coming from main.py : Error in /select-files/: {str(e)}")
        return {"error": "coming from main.py : Failed to process file selection"}


