# """
# ============================================================
# Disease Information Module

# Project : AI-Powered Plant Disease Detection System

# Purpose
# -------
# Provides disease information lookup:
# - Symptoms
# - Causes
# - Treatments
# - Prevention methods

# Source
# ------
# artifacts/disease_info.json

# Framework
# ----------
# Streamlit + TensorFlow
# ============================================================
# """


# # ==========================================================
# # PROJECT ROOT SETUP
# # ==========================================================

# import os
# import sys

# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

# if PROJECT_ROOT not in sys.path:
#     sys.path.insert(0, PROJECT_ROOT)



# # ==========================================================
# # IMPORTS
# # ==========================================================

# import json
# from pathlib import Path


# from config import (
#     DISEASE_INFO_FILE,
#     CACHE_DISEASE_INFO,
# )



# # ==========================================================
# # LOAD DISEASE INFORMATION
# # ==========================================================

# def load_disease_info():
#     """
#     Load disease information JSON.

#     Returns
#     -------
#     dict
#         Disease information database
#     """

#     disease_file = Path(DISEASE_INFO_FILE)


#     if not disease_file.exists():

#         raise FileNotFoundError(
#             f"Disease information file not found:\n{disease_file}"
#         )


#     with open(
#         disease_file,
#         "r",
#         encoding="utf-8"
#     ) as file:

#         return json.load(file)



# # ==========================================================
# # LOAD DATABASE
# # ==========================================================

# DISEASE_DATABASE = load_disease_info()



# # ==========================================================
# # DISEASE LOOKUP
# # ==========================================================

# def get_disease_details(disease_name):
#     """
#     Retrieve disease information.

#     Parameters
#     ----------
#     disease_name : str

#     Returns
#     -------
#     dict
#     """


#     if disease_name in DISEASE_DATABASE:

#         return DISEASE_DATABASE[disease_name]


#     return {
#         "name": disease_name,
#         "description": "Information not available.",
#         "symptoms": [],
#         "treatment": [],
#         "prevention": []
#     }



# # ==========================================================
# # INFORMATION HELPERS
# # ==========================================================

# def get_description(disease_name):

#     info = get_disease_details(disease_name)

#     return info.get(
#         "description",
#         "No description available."
#     )



# def get_symptoms(disease_name):

#     info = get_disease_details(disease_name)

#     return info.get(
#         "symptoms",
#         []
#     )



# def get_treatment(disease_name):

#     info = get_disease_details(disease_name)

#     return info.get(
#         "treatment",
#         []
#     )



# def get_prevention(disease_name):

#     info = get_disease_details(disease_name)

#     return info.get(
#         "prevention",
#         []
#     )



# # ==========================================================
# # TEST MODULE
# # ==========================================================

# if __name__ == "__main__":

#     print("=" * 60)
#     print("Disease Information Module Test")
#     print("=" * 60)


#     print(
#         "Disease file:",
#         DISEASE_INFO_FILE
#     )


#     print(
#         "Exists:",
#         Path(DISEASE_INFO_FILE).exists()
#     )


#     print(
#         "Loaded diseases:",
#         len(DISEASE_DATABASE)
#     )


#     if len(DISEASE_DATABASE) > 0:

#         first_disease = list(
#             DISEASE_DATABASE.keys()
#         )[0]


#         print(
#             "\nExample disease:"
#         )

#         print(
#             first_disease
#         )


#         print(
#             get_disease_details(first_disease)
#         )


#     print(
#         "\nDisease information module loaded successfully."
#     )
"""
============================================================
Disease Information Module

Project : AI-Powered Plant Disease Detection System
Purpose : Load and query agricultural information for crop diseases
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
from config import DISEASE_INFO_FILE

# ==========================================================
# CORE CORE FUNCTIONS
# ==========================================================

def load_disease_info():
    """
    Load the disease information dictionary from the configured JSON file path.

    Returns
    -------
    dict
        Dictionary containing comprehensive info for all configured plant classes.
    """
    file_path = Path(DISEASE_INFO_FILE)
    
    if not file_path.exists():
        print(f"Warning: Disease info file not found at {file_path}")
        return {}
        
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as error:
        print(f"Error reading disease info file: {error}")
        return {}

# Initialize cache
_DISEASE_DATA = load_disease_info()

def get_disease_details(disease_name):
    """
    Get full information object for a specific disease.
    """
    default_structure = {
        "description": "No information available for this class.",
        "symptoms": ["N/A"],
        "causes": ["N/A"],
        "treatment": ["N/A"],
        "prevention": ["N/A"]
    }
    return _DISEASE_DATA.get(disease_name, default_structure)

def get_description(disease_name):
    """
    Get the description string of a specific disease.
    """
    return get_disease_details(disease_name).get("description", "No description available.")

def get_symptoms(disease_name):
    """
    Get the list of symptoms for a specific disease.
    """
    return get_disease_details(disease_name).get("symptoms", [])

def get_causes(disease_name):
    """
    Get the list of causes/pathogens for a specific disease.
    """
    return get_disease_details(disease_name).get("causes", [])

def get_treatment(disease_name):
    """
    Get the list of treatment steps for a specific disease.
    """
    return get_disease_details(disease_name).get("treatment", [])

def get_prevention(disease_name):
    """
    Get the list of prevention steps for a specific disease.
    """
    return get_disease_details(disease_name).get("prevention", [])

# ==========================================================
# STANDALONE TEST
# ==========================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Disease Information Module Test")
    print("=" * 60)
    
    path_ref = Path(DISEASE_INFO_FILE)
    print(f"Disease file: {path_ref}")
    print(f"Exists: {path_ref.exists()}")
    print(f"Loaded diseases: {len(_DISEASE_DATA)}")
    print()
    
    example_key = "Apple_Apple Scab"
    print(f"Example disease:\n{example_key}")
    
    if example_key in _DISEASE_DATA:
        print(f"\nDescription:\n- {get_description(example_key)}")
        print("\nSymptoms:")
        for symptom in get_symptoms(example_key):
            print(f"  * {symptom}")
    else:
        print(f"\n[Error] Target example '{example_key}' was not found in the JSON data file.")
        
    print("\nDisease information module loaded successfully.")