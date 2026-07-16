"""
============================================================
Prediction Engine

Project : AI-Powered Plant Disease Detection
Dataset : PlantVillage Dataset (Tushar Sharma)

Purpose
-------
Loads trained models for inference.

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

from pathlib import Path
import time

import numpy as np
import streamlit as st
import tensorflow as tf

from config import (
    MODEL_PATHS,
    CLASS_NAMES,
    NUM_CLASSES,
    TOP_K,
    CONFIDENCE_DECIMALS,
    CUSTOM_CNN,
    FEATURE_EXTRACTION,
    FINE_TUNED,
    COMPARE_ALL,
)

# ==========================================================
# LOAD MODELS
# ==========================================================

@st.cache_resource(show_spinner="Loading AI models...")
def load_models():
    """
    Load and cache all trained TensorFlow models.

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

        try:
            models[model_name] = tf.keras.models.load_model(model_path)

        except Exception as error:
            raise RuntimeError(
                f"Failed to load '{model_name}' model.\n{error}"
            )

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

    print("\nAvailable Models")

    print(f"• {CUSTOM_CNN}")
    print(f"• {FEATURE_EXTRACTION}")
    print(f"• {FINE_TUNED}")
    print(f"• {COMPARE_ALL}")

    print("\nPrediction engine initialized successfully.")