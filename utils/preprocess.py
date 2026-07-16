"""
============================================================
Image Preprocessing Module

Project : AI-Powered Plant Disease Detection
Purpose : Prepare uploaded images for model prediction
============================================================
"""

import os
import sys

# ==========================================================
# MAKE PROJECT ROOT IMPORTABLE
# ==========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ==========================================================
# IMPORTS
# ==========================================================

from PIL import Image
import numpy as np

from config import (
    IMAGE_SIZE,
    ALLOWED_IMAGE_TYPES,
)

# ==========================================================
# VALIDATE IMAGE
# ==========================================================

def validate_image(uploaded_file):
    """
    Validate uploaded image type.
    """

    if uploaded_file is None:
        return False

    extension = uploaded_file.name.split(".")[-1].lower()

    return extension in ALLOWED_IMAGE_TYPES


# ==========================================================
# LOAD IMAGE
# ==========================================================

def load_image(uploaded_file):
    """
    Load uploaded image and convert to RGB.
    """

    image = Image.open(uploaded_file)

    return image.convert("RGB")


# ==========================================================
# RESIZE IMAGE
# ==========================================================

def resize_image(image):
    """
    Resize image to model input size.
    """

    return image.resize(IMAGE_SIZE)


# ==========================================================
# CONVERT TO NUMPY
# ==========================================================

def image_to_array(image):
    """
    Convert PIL image to NumPy array.

    IMPORTANT
    ---------
    No normalization is performed here.

    The trained models already contain
    their preprocessing layers.
    """

    return np.asarray(image, dtype=np.float32)


# ==========================================================
# ADD BATCH DIMENSION
# ==========================================================

def add_batch_dimension(image_array):
    """
    Convert

    (224,224,3)

    into

    (1,224,224,3)
    """

    return np.expand_dims(image_array, axis=0)


# ==========================================================
# COMPLETE PREPROCESSING PIPELINE
# ==========================================================

def preprocess_image(uploaded_file):
    """
    Complete preprocessing pipeline.

    Upload
        ↓
    RGB Conversion
        ↓
    Resize
        ↓
    NumPy Array
        ↓
    Batch Dimension

    Returns
    -------
    numpy.ndarray
    """

    image = load_image(uploaded_file)

    image = resize_image(image)

    image_array = image_to_array(image)

    image_array = add_batch_dimension(image_array)

    return image_array


# ==========================================================
# PREPROCESS EXISTING PIL IMAGE
# ==========================================================

def preprocess_pil_image(image):
    """
    Preprocess a PIL Image object.
    """

    image = image.convert("RGB")

    image = resize_image(image)

    image_array = image_to_array(image)

    image_array = add_batch_dimension(image_array)

    return image_array


# ==========================================================
# TEST MODULE
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Plant Disease Detection")
    print("Image Preprocessing Module")
    print("=" * 60)

    print("\nConfiguration")

    print(f"Image Size : {IMAGE_SIZE}")

    print(f"Supported Types : {ALLOWED_IMAGE_TYPES}")

    print("\nModule imported successfully.")

    print("\nReady for prediction pipeline.")