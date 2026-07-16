"""
============================================================
Image Preprocessing Module

Project : AI-Powered Plant Disease Detection
Purpose : Prepare uploaded images for model prediction
============================================================
"""

from PIL import Image
import numpy as np

from config import (
    IMAGE_SIZE,
    ALLOWED_IMAGE_TYPES
)


def validate_image(uploaded_file):
    """
    Validate uploaded image type.
    """

    if uploaded_file is None:
        return False

    extension = uploaded_file.name.split(".")[-1].lower()

    return extension in ALLOWED_IMAGE_TYPES


def load_image(uploaded_file):
    """
    Load uploaded image and convert to RGB.
    """

    image = Image.open(uploaded_file)

    return image.convert("RGB")


def resize_image(image):
    """
    Resize image to model input size.
    """

    return image.resize(IMAGE_SIZE)


def image_to_array(image):
    """
    Convert PIL image to NumPy array.

    NOTE:
    Do NOT normalize here because preprocessing is already
    embedded inside the trained models.
    """

    return np.asarray(image, dtype=np.float32)


def add_batch_dimension(image_array):
    """
    Convert

        (224,224,3)

    into

        (1,224,224,3)
    """

    return np.expand_dims(image_array, axis=0)


def preprocess_image(uploaded_file):
    """
    Complete preprocessing pipeline.

    Upload
        ↓
    RGB
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


def preprocess_pil_image(image):
    """
    Preprocess an existing PIL image.
    Useful for testing.
    """

    image = image.convert("RGB")

    image = resize_image(image)

    image_array = image_to_array(image)

    image_array = add_batch_dimension(image_array)

    return image_array