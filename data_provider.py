from collections import defaultdict
from typing import List
import os

from logger_config import setup_logger
logger = setup_logger("data_provider")

def receive_files(folder_path: str, file_list: List[str]):
    logger.info("                                                             ")
    logger.info("[DATA PROVIDER] Data received in data_provider.py")
    logger.info(f"[DATA PROVIDER] Folder Path: {folder_path}")
    logger.info(f"[DATA PROVIDER] File List: {file_list}")
    logger.info("                                                             ")

    # Grouping definitions
    extension_map = {
        "excel": ["xls", "xlsx", "csv", "xlsm"],
        "powerpoint": ["ppt", "pptx", "pptm"],
        "word": ["doc", "docx"],
        "pdf": ["pdf"],
        "text": ["txt"]
    }

    grouped_files_by_type = defaultdict(list)

    for file in file_list:
        ext = os.path.splitext(file)[1].lower().strip(".")
        for group, extensions in extension_map.items():
            if ext in extensions:
                grouped_files_by_type[group].append(file)
                break
        else:
            grouped_files_by_type["other"].append(file)

    final_list_of_lists = [
        grouped_files_by_type.get("excel", []),
        grouped_files_by_type.get("pdf", []),
        grouped_files_by_type.get("powerpoint", []),
        grouped_files_by_type.get("text", []),
        grouped_files_by_type.get("word", []),
        grouped_files_by_type.get("other", [])
    ]

    logger.info(f"[DATA PROVIDER] Final grouped list of lists: {final_list_of_lists}")
