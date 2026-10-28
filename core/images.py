"""Validate and normalise uploaded site photos before they reach the model."""

import io

from PIL import Image, UnidentifiedImageError

from config.settings import MAX_IMAGE_BYTES, MAX_IMAGE_DIMENSION


class ImageLoadError(ValueError):
    """The uploaded file is missing, too large, or not a readable image."""


def load_image_bytes(data: bytes) -> Image.Image:
    if not data:
        raise ImageLoadError("The uploaded file is empty.")
    if len(data) > MAX_IMAGE_BYTES:
        raise ImageLoadError("The image is larger than 15 MB. Please upload a smaller file.")
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError) as exc:
        raise ImageLoadError("Could not read the image. Please upload a valid JPG or PNG.") from exc

    image = image.convert("RGB")
    image.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION))
    return image


def load_image(uploaded_file) -> Image.Image:
    """Accepts a Streamlit UploadedFile (anything exposing getvalue())."""
    return load_image_bytes(uploaded_file.getvalue())
