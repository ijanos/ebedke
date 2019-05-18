from base64 import b64encode
from datetime import datetime
import unicodedata

import requests

from ebedke.utils import http
from ebedke import settings

VISION_API_ROOT = "https://vision.googleapis.com/v1/images:annotate"

days_lower = ["hétfő", "kedd", "szerda", "csütörtök", "péntek", "szombat", "vasárnap"]
days_lower_ascii = ["hetfo", "kedd", "szerda", "csutortok", "pentek", "szombat", "vasarnap"]
days_upper = [day.upper() for day in days_lower]

months_hu_capitalized = ["Január", "Február", "Március",
                         "Április", "Május", "Június",
                         "Július", "Augusztus", "Szeptember",
                         "Október", "November", "December"]


def get_fresh_image(url, fresh_date):
    response = http.get(url)
    lastmod = response.headers.get('last-modified')
    if not lastmod:
        print("[ebedke] image is missing last-modified header")
        return None
    lastmod = datetime.strptime(lastmod, '%a, %d %b %Y %H:%M:%S %Z')
    if lastmod >= fresh_date:
        return response.content
    else:
        return None

def content_size_match(url, expected_size):
    response = requests.head(url)
    return response.headers['content-length'] == expected_size

def skip_empty_lines(text):
    for line in text:
        line = line.strip()
        if len(line) > 1:
            yield line

def ocr_image(image, langHint="hu"):
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
    return response.json()['responses'][0]['textAnnotations'][0]['description']


def workday(date):
    datestr = date.strftime("%Y-%m-%d")
    extra_workdays = [
        "2019-08-10", "2019-12-07", "2019-12-14"
    ]

    if datestr in extra_workdays:
        return True

    holidays = [
        "2018-12-31", "2019-01-01", "2019-03-15", "2019-04-19", "2019-04-22", "2019-05-01",
        "2019-06-10", "2019-08-19", "2019-08-20", "2019-10-23", "2019-11-01", "2019-12-24",
        "2019-12-25", "2019-12-26", "2019-12-27"
    ]

    if datestr in holidays:
        return False

    return date.weekday() < 5

def on_workdays(func):
    def wrapper(*args, **kwargs):
        if not workday(args[0]):
            return []
        else:
            return func(*args, **kwargs)
    return wrapper

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

def remove_accents(text):
    nfkd = unicodedata.normalize('NFKD', text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))
