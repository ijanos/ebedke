from io import BytesIO
from base64 import b64encode

from PIL import Image
import requests
from ebedke.utils import http
from ebedke import settings


VISION_API_ROOT = "https://vision.googleapis.com/v1/images:annotate"

def load_img(url: str) -> Image:
    image = http.get_bytes(url)
    return Image.open(BytesIO(image))


def ocr_image(img_bytes: bytes, langHint: str = "hu") -> str:
    img_request = {"requests": [{
        "image": {"content": b64encode(img_bytes).decode('ascii')},
        "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
        "imageContext": {"languageHints": [langHint]}
    }]}
    response = requests.post(VISION_API_ROOT, json=img_request,
                             params={'key': settings.google_token},
                             headers={'Content-Type': 'application/json'},
                             timeout=10)
    if response.status_code != 200 or response.json().get('error'):
        print("[ebedke] Google OCR error", response.text)
        return ""

    text_content = response.json()['responses'][0]['textAnnotations'][0]['description']

    if text_content and isinstance(text_content, str):
        return text_content
    else:
        return ""
