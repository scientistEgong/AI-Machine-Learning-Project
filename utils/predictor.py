"""
============================================================
Prediction Engine

Project : AI-Powered Plant Disease Detection
Dataset : PlantVillage Dataset (Tushar Sharma)

Purpose
-------
Loads trained models and class labels for inference.

This module serves as the central prediction engine for the
entire Streamlit application.
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

import streamlit as st
import tensorflow as tf

from config import (
    MODEL_PATHS,
)

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(PROJECT_ROOT)

ARTIFACTS_DIR = BASE_DIR / "artifacts"

CLASS_NAMES_PATH = ARTIFACTS_DIR / "class_names.json"

# ==========================================================
# LOAD CLASS NAMES
# ==========================================================

def load_class_names():
    """
    Load class names from JSON file.

    Returns
    -------
    list[str]
        Ordered list of class labels used during training.
    """

    if not CLASS_NAMES_PATH.exists():
        raise FileNotFoundError(
            f"Class names file not found:\n{CLASS_NAMES_PATH}"
        )

    with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
        class_names = json.load(file)

    return class_names


CLASS_NAMES = load_class_names()

NUM_CLASSES = len(CLASS_NAMES)

# ==========================================================
# LOAD MODELS
# ==========================================================

@st.cache_resource
def load_models():
    """
    Load all trained TensorFlow models.

    Models are cached so they are only loaded once
    during the Streamlit session.

    Returns
    -------
    dict
        Dictionary containing all loaded models.
    """

    models = {}

    for model_name, model_path in MODEL_PATHS.items():

        model_path = Path(model_path)

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found:\n{model_path}"
            )

        models[model_name] = tf.keras.models.load_model(model_path)

    return models

# ==========================================================
# INITIALIZE MODEL CACHE
# ==========================================================

MODELS = load_models()

# ==========================================================
# STANDALONE TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Prediction Engine")
    print("=" * 60)

    print("\nLoaded Models")

    for model_name in MODELS:
        print(f"✓ {model_name}")

    print(f"\nNumber of Classes : {NUM_CLASSES}")

    print("\nFirst Five Classes")

    for label in CLASS_NAMES[:5]:
        print(f" - {label}")

    print("\nPrediction engine initialized successfully.")