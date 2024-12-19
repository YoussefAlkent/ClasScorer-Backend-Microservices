import base64
from io import BytesIO
from fastapi import HTTPException
from PIL import Image

def decode_image(encoded_image: str) -> Image.Image:
    """
    Decode a base64-encoded image into a PIL Image.
    """
    try:
        image_data = base64.b64decode(encoded_image)
        return Image.open(BytesIO(image_data)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image format")
