def my_function():
    return {"message": "Hello from my_function!"}
import os

import os
from app.console_logger import log_stage

def get_survey_info(directory_path: str) -> dict:
    """
    Retrieves information about survey files in the given directory.
    
    Args:
        directory_path (str): The path to the directory to scan.

    Returns:
        dict: A dictionary containing:
            - 'exists' (bool): True if directory exists, False otherwise.
            - 'file_count' (int): Number of files in the directory.
            - 'file_names' (list): List of filenames.
    """
    log_stage("Checking Survey Directory... 📂", f"Looking into {directory_path}")

    if not os.path.exists(directory_path):
        result = {"exists": False, "file_count": 0, "file_names": []}
        log_stage("Directory Not Found! ❌", "Returning default empty response.", result)
        return result

    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    result = {"exists": True, "file_count": len(files), "file_names": files}

    log_stage("Survey Info Retrieved! ✅", f"Found {len(files)} file(s).", result)
    return result

def get_resident_survey_info() -> dict:
    """Wrapper function to get resident survey info."""
    return get_survey_info(os.path.join(os.getcwd(), "surveys", "resident"))

def get_stakeholder_survey_info() -> dict:
    """Wrapper function to get stakeholder survey info."""
    return get_survey_info(os.path.join(os.getcwd(), "surveys", "stakeholder"))
