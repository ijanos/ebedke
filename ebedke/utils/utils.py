from base64 import b64encode
from io import BytesIO
import requests
from ebedke import settings

VISION_API_ROOT = "https://vision.googleapis.com/v1/images:annotate"


def content_size_match(url, expected_size):
    response = requests.head(url)
    return response.headers['content-length'] == expected_size

def skip_empty_lines(text):
    for line in text:
        line = line.strip()
        if len(line) > 1:
            yield line

def ocr_image(image: BytesIO, langHint: str = "hu") -> str:
    img_request = {"requests": [{
        "image": {"content": b64encode(image.getvalue()).decode('ascii')},
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
    desc = response.json()['responses'][0]['textAnnotations'][0]['description']
    if isinstance(desc, str):
        return desc
    else:
        print("Description is not a string")
        return ""


def pattern_slice(iterator, start_patterns, end_patterns, inclusive=False, modifier=str.lower):
    drop = True
    for i in iterator:
        if drop and any(p in modifier(i) for p in start_patterns):
            drop = False
            if inclusive:
                yield i
        elif not drop and any(p in modifier(i) for p in end_patterns):
            break
        elif not drop:
            yield i
