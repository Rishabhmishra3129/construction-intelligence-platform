import io

import pytest
from PIL import Image

from config.settings import MAX_IMAGE_DIMENSION
from core.images import ImageLoadError, load_image_bytes
from core.render_prompt import build_render_prompt, build_render_url


def _png_bytes(size=(3000, 2000)):
    buf = io.BytesIO()
    Image.new("RGB", size, (120, 120, 120)).save(buf, format="PNG")
    return buf.getvalue()


def test_large_images_are_downscaled():
    img = load_image_bytes(_png_bytes())
    assert max(img.size) <= MAX_IMAGE_DIMENSION
    assert img.mode == "RGB"


def test_invalid_bytes_raise_friendly_error():
    with pytest.raises(ImageLoadError):
        load_image_bytes(b"not an image")


def test_empty_upload_rejected():
    with pytest.raises(ImageLoadError):
        load_image_bytes(b"")


def test_render_prompt_mentions_key_details():
    prompt = build_render_prompt("Independent Villa", 2500, "Tier 2 (Large City)")
    assert "independent villa" in prompt
    assert "2,500 square feet" in prompt
    assert "Tier 2" in prompt


def test_render_url_is_encoded_and_parameterised():
    url = build_render_url("modern villa & pool")
    assert url.startswith("https://image.pollinations.ai/prompt/")
    assert "modern%20villa%20%26%20pool" in url
    assert "nologo=true" in url
