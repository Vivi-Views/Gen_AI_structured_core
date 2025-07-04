# === Imports === #

# imports FastAPI
from fastapi import FastAPI

# === Imports === #


# ================= Invoke Module code ================= #

# path_files_selector.py module
# from path_files_selector import FileSelectorModule

# logger_config.py module
from logger_config import setup_logger
logger = setup_logger("main")

# data_provider.py module
from data_provider import get_prepared_files

# ================= Invoke Module code ================= #




# ==== Fast API initialization ==== #

# Initializes the FastAPI app to expose endpoints for each resume section extraction.
app = FastAPI()

# CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://127.0.0.1:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==== Webpage check ==== #
# paste this in a fresh web-page (http://127.0.0.1:8000)
@app.get("/")
def read_root():
    return {"message": "Xiphold project is up and running !!!"}

# ================= XXX ================= #
# Explanation so far
# main.py, import FastAPI, app-fastapi, @app.get("/")-def read_root()
# cmd.bat, uvicorn main:app --reload, http://127.0.0.1:8000, chk webpage
# ================= XXX ================= #












# ================= XXX ================= #

# Testing path_files_selector.py code

from fastapi import Request
from typing import List
from path_files_selector import FileSelectorModule


@app.post("/select-files/")
async def select_files_endpoint(request: Request):
    try:

        logger.info("# ================= Started New Iteration ================= #")
        logger.info("coming from main.py - API called : /select-files/")

        body = await request.json()
        files: List[str] = body.get("file_paths", [])
        logger.info(f"coming from main.py - API called : Files received from frontend: {files}")

        selector = FileSelectorModule()
        folder_path, file_list = selector.process_selected_files(files)

        return {
            "folder_path": folder_path,
            "files": file_list
        }

    except Exception as e:
        logger.error("# ================================================== #")
        logger.error(f"coming from main.py - Error in /select-files/: {str(e)}")
        return {"coming from main.py - error": "Failed to process file selection"}

# ================= XXX ================= #

from fastapi.responses import PlainTextResponse
from data_provider import get_prepared_files

@app.get("/print-selected-files/", response_class=PlainTextResponse)
async def print_selected_files():
    prepared_files = get_prepared_files()
    if not prepared_files:
        return "No files selected yet."
    return "\n".join(prepared_files)







