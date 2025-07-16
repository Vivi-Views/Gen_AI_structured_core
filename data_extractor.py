# === Imports === #
import os
from typing import List
from logger_config import setup_logger
from unstructured.partition.auto import partition

data_extractor_logger = setup_logger("data_extractor")

# === Output Folder === #
RAW_TEXT_OUTPUT_DIR = r"C:\Users\vivek\Desktop\Xiphold\raw_texts"

# === Entry Point === #	
def receive_files(folder_path: str, file_list: List[str]):
    data_extractor_logger.info("                                                             ")
    data_extractor_logger.info("[DATA EXTRACTOR] Data received in data_extractor.py")
    data_extractor_logger.info(f"[DATA EXTRACTOR] Folder Path: {folder_path}")
    data_extractor_logger.info(f"[DATA EXTRACTOR] File List: {file_list}")
    data_extractor_logger.info("                                                             ")

    # === Construct full file paths ===
    full_paths = [os.path.join(folder_path, file) for file in file_list]
    data_extractor_logger.info(f"[DATA EXTRACTOR] Full file paths: {full_paths}")

    # === Iterate through each file ===
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        try:
            data_extractor_logger.info(f"[DATA EXTRACTOR] Now processing: {file_path}")
            # 🔧 TODO: Add your extraction logic here (e.g., unstructured.partition)
        except Exception as e:
            data_extractor_logger.error(f"[DATA EXTRACTOR] Failed to process {file_path}: {str(e)}")
            
            def extract_and_save_text(file_path: str):
                try:
                    # Extract elements using Unstructured's auto-partitioner
                    elements = partition(filename=file_path)
                    extracted_text = "\n".join(str(el) for el in elements).strip()

                    # Create output directory if not exists
                    os.makedirs(RAW_TEXT_OUTPUT_DIR, exist_ok=True)

                    # Build .txt output path
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_txt_path = os.path.join(RAW_TEXT_OUTPUT_DIR, f"{base_name}.txt")

                    # Save the extracted text
                    with open(output_txt_path, "w", encoding="utf-8") as f:
                        f.write(extracted_text)

                    data_extractor_logger.info(f"[DATA EXTRACTOR] Extracted and saved: {output_txt_path}")
                except Exception as e:
                    data_extractor_logger.error(f"[DATA EXTRACTOR] Extraction failed for {file_path}: {str(e)}")




