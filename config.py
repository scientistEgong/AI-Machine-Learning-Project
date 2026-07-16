"""
============================================================
Configuration File
Project : AI-Powered Plant Disease Detection System
Dataset : PlantVillage Dataset (Tushar Sharma)
Framework : Streamlit + TensorFlow
============================================================
"""

import json
from pathlib import Path

# ==========================================================
# APPLICATION SETTINGS
# ==========================================================

APP_TITLE = "AI-Powered Plant Disease Detection"

APP_ICON = "🌿"

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

VERSION = "1.0.0"

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

MODELS_DIR = BASE_DIR / "models"

ARTIFACTS_DIR = BASE_DIR / "artifacts"

ASSETS_DIR = BASE_DIR / "assets"

UTILS_DIR = BASE_DIR / "utils"

PAGES_DIR = BASE_DIR / "pages"

REPORTS_DIR = BASE_DIR / "reports"

OUTPUTS_DIR = BASE_DIR / "outputs"

SAMPLE_IMAGES_DIR = BASE_DIR / "sample_images"

# ==========================================================
# MODEL NAMES
# ==========================================================

CUSTOM_CNN = "Custom CNN"

FEATURE_EXTRACTION = "Feature Extraction"

FINE_TUNED = "Fine-Tuned MobileNetV3"

COMPARE_ALL = "Compare All Models"

# ==========================================================
# MODEL FILES
# ==========================================================

MODEL_PATHS = {
    CUSTOM_CNN: MODELS_DIR / "custom_cnn_final.keras",
    FEATURE_EXTRACTION: MODELS_DIR / "tl_feature_extraction_final.keras",
    FINE_TUNED: MODELS_DIR / "tl_finetuned_final.keras",
}

DEFAULT_MODEL = FINE_TUNED

AVAILABLE_MODELS = [
    CUSTOM_CNN,
    FEATURE_EXTRACTION,
    FINE_TUNED,
    COMPARE_ALL,
]

# ==========================================================
# MODEL INFORMATION
# ==========================================================

MODEL_INFORMATION = {
    CUSTOM_CNN: {
        "architecture": "Custom CNN",
        "description": "CNN model developed from scratch."
    },

    FEATURE_EXTRACTION: {
        "architecture": "MobileNetV3",
        "description": "Transfer learning using frozen feature extraction."
    },

    FINE_TUNED: {
        "architecture": "MobileNetV3",
        "description": "Transfer learning with fine-tuning."
    }
}

# ==========================================================
# IMAGE SETTINGS
# ==========================================================

IMAGE_HEIGHT = 224

IMAGE_WIDTH = 224

IMAGE_CHANNELS = 3

IMAGE_SIZE = (IMAGE_HEIGHT, IMAGE_WIDTH)

# ==========================================================
# FILE SETTINGS
# ==========================================================

ALLOWED_IMAGE_TYPES = [
    "jpg",
    "jpeg",
    "png"
]

MAX_FILE_SIZE_MB = 10

# ==========================================================
# PREDICTION SETTINGS
# ==========================================================

TOP_K = 5

CONFIDENCE_DECIMALS = 2

SHOW_TOP_PREDICTIONS = True

SHOW_CONFIDENCE = True

# ==========================================================
# STREAMLIT THEME
# ==========================================================

PRIMARY_COLOR = "#2ECC71"

BACKGROUND_COLOR = "#090A0C"

SURFACE_COLOR = "#161A20"

TEXT_COLOR = "#F3F4F6"

SUCCESS_COLOR = "#2ECC71"

WARNING_COLOR = "#E67E22"

ERROR_COLOR = "#E74C3C"

# ==========================================================
# PAGE TITLES
# ==========================================================

HOME_PAGE = "🏠 Home"

DETECTION_PAGE = "🔬 Disease Detection"

PERFORMANCE_PAGE = "📊 Model Performance"

LIBRARY_PAGE = "📖 Disease Library"

ABOUT_PAGE = "ℹ️ About"

# ==========================================================
# CLASS LABELS
# ==========================================================

# CLASS_NAMES_FILE = ARTIFACTS_DIR / "class_names.json"
# print("=" * 60)
# print("CLASS_NAMES_FILE:", CLASS_NAMES_FILE)
# print("Exists:", CLASS_NAMES_FILE.exists())
# print("=" * 60)
# if CLASS_NAMES_FILE.exists():
#     with open(CLASS_NAMES_FILE, "r", encoding="utf-8") as file:
#         CLASS_NAMES = json.load(file)
# else:
#     CLASS_NAMES = []

# NUM_CLASSES = len(CLASS_NAMES)
# print("Loaded classes:", len(CLASS_NAMES))
CLASS_NAMES_FILE = ARTIFACTS_DIR / "class_names.json"

print("=" * 60)
print("CLASS_NAMES_FILE:", CLASS_NAMES_FILE)
print("Exists:", CLASS_NAMES_FILE.exists())

if CLASS_NAMES_FILE.exists():
    with open(CLASS_NAMES_FILE, "r", encoding="utf-8") as file:
        CLASS_NAMES = json.load(file)

    print("Type:", type(CLASS_NAMES))
    print("Length:", len(CLASS_NAMES))

    if len(CLASS_NAMES) > 0:
        print("First class:", CLASS_NAMES[0])

else:
    print("File not found!")
    CLASS_NAMES = []

NUM_CLASSES = len(CLASS_NAMES)
print("NUM_CLASSES =", NUM_CLASSES)
print("=" * 60)

# ==========================================================
# DISEASE INFORMATION
# ==========================================================

DISEASE_INFO_FILE = ARTIFACTS_DIR / "disease_info.json"

if DISEASE_INFO_FILE.exists():
    with open(DISEASE_INFO_FILE, "r", encoding="utf-8") as file:
        DISEASE_INFO = json.load(file)
else:
    DISEASE_INFO = {}

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

PROJECT_NAME = "AI-Powered Plant Disease Detection"

DATASET = "PlantVillage Dataset"

MODEL_FRAMEWORK = "TensorFlow"

TRANSFER_MODEL = "MobileNetV3"

AUTHOR = "Scientist Egong"

ACADEMIC_YEAR = "2026"

LICENSE = "MIT"

# ==========================================================
# FEATURE FLAGS
# ==========================================================

ENABLE_MODEL_CACHE = True

ENABLE_GPU = True

ENABLE_HISTORY = True

ENABLE_PDF_REPORT = True

ENABLE_GRADCAM = False

ENABLE_MODEL_COMPARISON = True

# ==========================================================
# CACHE SETTINGS
# ==========================================================

CACHE_MODELS = True

CACHE_DISEASE_INFO = True

CACHE_CLASS_NAMES = True
print(BASE_DIR)