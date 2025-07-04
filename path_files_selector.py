import os
from typing import List, Tuple
from pathlib import Path

from logger_config import setup_logger
logger = setup_logger("FileSelector")

class FileSelectorModule:
    def __init__(self):
        self.folder_path: str = ""
        self.selected_files: List[str] = []

    def process_selected_files(self, full_file_paths: List[str]) -> Tuple[str, List[str]]:
        """
        Accepts a list of full file paths, extracts folder path and filenames.

        :param full_file_paths: List of full file paths from frontend
        :return: Tuple of folder path and list of filenames
        """

        try:
            logger.info("                                                             ")
            logger.info("[PATH FILES SELECTOR] main.py is sending the file names into this function.")
            print("[PATH FILES SELECTOR] main.py is sending the file names into this function.")

            if not full_file_paths:
                raise ValueError("No files selected")

            # Store the folder path from first file
            self.folder_path = str(Path(full_file_paths[0]).parent)
            print(f"[PATH FILES SELECTOR] Folder path : {self.folder_path}")

            # Extract filenames only
            self.selected_files = [os.path.basename(file_path) for file_path in full_file_paths]
            print(f"[PATH FILES SELECTOR] Files : {self.selected_files}")

            logger.info(f"[PATH FILES SELECTOR] Folder path resolved: {self.folder_path}")
            logger.info("webpage will not give the absolute path of the files for security reasons.")
            logger.info(f"[PATH FILES SELECTOR] Files extracted: {self.selected_files}")
            logger.info("                                                             ")

            return self.folder_path, self.selected_files

        except Exception as e:
            logger.info("                                                             ")
            logger.error(f"[PATH FILES SELECTOR] Error in processing file paths: {str(e)}")
            logger.info("                                                             ")
            raise
    

