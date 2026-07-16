"""
============================================================
Helper Utilities

Project : AI-Powered Plant Disease Detection System

Purpose
-------
Common reusable helper functions for:
- File validation
- Directory handling
- JSON operations
============================================================
"""


# ==========================================================
# PROJECT ROOT SETUP
# ==========================================================

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ==========================================================
# IMPORTS
# ==========================================================

import json
from pathlib import Path


from config import (
    BASE_DIR,
    ARTIFACTS_DIR,
    OUTPUTS_DIR,
    REPORTS_DIR,
)


# ==========================================================
# PATH UTILITIES
# ==========================================================

def ensure_directory(directory):
    """
    Create directory if it does not exist.

    Parameters
    ----------
    directory : Path or str

    Returns
    -------
    Path
    """

    directory = Path(directory)

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return directory



def file_exists(file_path):
    """
    Check if file exists.
    """

    return Path(file_path).exists()



def get_project_path(*paths):
    """
    Build paths from project root.

    Example:
        get_project_path("models", "model.keras")
    """

    return BASE_DIR.joinpath(*paths)



# ==========================================================
# JSON UTILITIES
# ==========================================================

def load_json(file_path):
    """
    Load JSON file.

    Returns
    -------
    dict/list
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"JSON file not found:\n{file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def save_json(data, file_path):
    """
    Save data as JSON.
    """

    file_path = Path(file_path)

    ensure_directory(
        file_path.parent
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )



# ==========================================================
# IMAGE / FILE VALIDATION
# ==========================================================

def validate_file_extension(
        filename,
        allowed_extensions
):
    """
    Validate file extension.

    Example:
        validate_file_extension(
            "leaf.jpg",
            ["jpg","png"]
        )
    """

    extension = (
        Path(filename)
        .suffix
        .replace(".", "")
        .lower()
    )

    return extension in allowed_extensions



# ==========================================================
# APPLICATION FOLDERS
# ==========================================================

def create_application_directories():
    """
    Ensure required runtime folders exist.
    """

    folders = [
        OUTPUTS_DIR,
        REPORTS_DIR,
    ]

    for folder in folders:
        ensure_directory(folder)



# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Helper Utilities Test")
    print("=" * 60)

    print(
        "Project Root:",
        BASE_DIR
    )

    print(
        "Artifacts:",
        ARTIFACTS_DIR
    )

    print(
        "Outputs:",
        OUTPUTS_DIR
    )

    print(
        "Reports:",
        REPORTS_DIR
    )

    print("\nHelpers loaded successfully.")