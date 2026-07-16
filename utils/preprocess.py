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
    Validate uploaded image file.

    Parameters
    ----------
    uploaded_file : UploadedFile
        Streamlit uploaded file object.

    Returns
    -------
    bool
        True if file extension is supported.
    """

    if uploaded_file is None:
        return False

    extension = uploaded_file.name.split(".")[-1].lower()

    return extension in ALLOWED_IMAGE_TYPES


def load_image(uploaded_file):
    """
    Open uploaded image and convert to RGB.

    Parameters
    ----------
    uploaded_file : UploadedFile

    Returns
    -------
    PIL.Image.Image
    """

    image = Image.open(uploaded_file)

    image = image.convert("RGB")

    return image


def resize_image(image):
    """
    Resize image to model input size.

    Parameters
    ----------
    image : PIL.Image.Image

    Returns
    -------
    PIL.Image.Image
    """

    return image.resize(IMAGE_SIZE)


def image_to_array(image):
    """
    Convert PIL image to NumPy array.

    Parameters
    ----------
    image : PIL.Image.Image

    Returns
    -------
    numpy.ndarray
    """

    return np.array(image, dtype=np.float32)


def normalize_image(image_array):
    """
    Normalize pixel values to [0,1].

    Parameters
    ----------
    image_array : numpy.ndarray

    Returns
    -------
    numpy.ndarray
    """

    return image_array / 255.0


def add_batch_dimension(image_array):
    """
    Add batch dimension.

    (224,224,3)
        ↓
    (1,224,224,3)

    Parameters
    ----------
    image_array : numpy.ndarray

    Returns
    -------
    numpy.ndarray
    """

    return np.expand_dims(image_array, axis=0)


def preprocess_image(uploaded_file):
    """
    Complete preprocessing pipeline.

    Pipeline
    --------
    Upload
        ↓
    RGB Conversion
        ↓
    Resize
        ↓
    NumPy Array
        ↓
    Normalize
        ↓
    Batch Dimension

    Parameters
    ----------
    uploaded_file : UploadedFile

    Returns
    -------
    numpy.ndarray
        Model-ready image tensor.
    """

    image = load_image(uploaded_file)

    image = resize_image(image)

    image_array = image_to_array(image)

    image_array = normalize_image(image_array)

    image_array = add_batch_dimension(image_array)

    return image_array


def preprocess_pil_image(image):
    """
    Preprocess an existing PIL Image.

    Useful for testing or future API integration.

    Parameters
    ----------
    image : PIL.Image.Image

    Returns
    -------
    numpy.ndarray
    """

    image = image.convert("RGB")

    image = resize_image(image)

    image_array = image_to_array(image)

    image_array = normalize_image(image_array)

    image_array = add_batch_dimension(image_array)

    return image_array