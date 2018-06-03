from  urllib.parse import urlencode
from base64 import b64encode
from datetime import datetime
from functools import partial
import operator
import pickle
import unicodedata

import requests
from lxml import html
import redis

import config


FB_TOKEN = urlencode({"access_token": config.FB_ACCESS_TOKEN})
FB_API_ROOT = "https://graph.facebook.com/v2.11"
VISION_API_ROOT = "https://vision.googleapis.com/v1/images:annotate"


HEADERS = {
    'User-Agent': config.USER_AGENT,
}

days_lower = ["hétfő", "kedd", "szerda", "csütörtök", "péntek", "szombat", "vasárnap"]
days_lower_ascii = ["hetfo", "kedd", "szerda", "csutortok", "pentek", "szombat", "vasarnap"]
days_upper = [day.upper() for day in days_lower]

DEBUG_CACHE = None

def http_get(url, params=None):
    global DEBUG_CACHE

    headers = {
        'User-Agent': config.USER_AGENT,
    }
    get = partial(requests.get, headers=headers, params=params, timeout=config.REQUEST_TIMEOUT)

    if config.PERSISTENT_CACHE:
        if not DEBUG_CACHE:
            DEBUG_CACHE = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=False)

        cached = DEBUG_CACHE.get(url)
        if not cached:
            print("[ebedke] saving to redis cache\n")
            cached = get(url)
            DEBUG_CACHE.set(url, pickle.dumps(cached), ex=3600)
            response = cached
        else:
            print("[ebedke] loaded from redis cache\n")
            response = pickle.loads(cached)
    else:
        response = get(url)

    return response

def get_dom(url, force_utf8=False):
    response = http_get(url)
    if force_utf8:
        response.encoding = 'utf-8'
    return html.fromstring(response.text)

def get_fresh_image(url, fresh_date):
    response = http_get(url)
    lastmod = response.headers.get('last-modified')
    if not lastmod:
        print("[ebedke] image is missing last-modified header")
        return None
    lastmod = datetime.strptime(lastmod, '%a, %d %b %Y %H:%M:%S %Z')
    if lastmod >= fresh_date:
        return response.content
    else:
        return None

def get_filtered_fb_post(page_id, post_filter):
    payload = {
        "limit": 10,
        "access_token": config.FB_ACCESS_TOKEN
    }
    response = http_get(f"{ FB_API_ROOT }/{ page_id }/posts", params=payload)
    json = response.json()
    if "error" in json:
        print("[ebedke] Facebook API error:", json['error']['message'])
        return ""
    posts = json['data']
    for post in posts:
        if "message" in post and post_filter(post):
            return post["message"]
    return ""

def get_post_attachments(post_id):
    url = f"{ FB_API_ROOT }/{ post_id }/attachments?{ FB_TOKEN }"
    return http_get(url).json()

def get_fb_post_attached_image(page_id, post_filter):
    payload = {
        "fields": "message,created_time,attachments{target{id}}",
        "limit": 8,
        "access_token": config.FB_ACCESS_TOKEN
    }
    response = http_get(f"{ FB_API_ROOT }/{ page_id }/posts", params=payload)
    posts = response.json()['data']
    post = None
    for p in posts:
        if "message" in p and post_filter(p):
            post = p
            break
    if post:
        attachments_id = post["attachments"]["data"][0]["target"]["id"]
        payload = {
            "fields": "images",
            "access_token": config.FB_ACCESS_TOKEN
        }
        response = http_get(f"{ FB_API_ROOT }/{ attachments_id }", params=payload)
        images = response.json()["images"]
        large_image = max(images, key=operator.itemgetter("height"))
        return http_get(large_image["source"]).content
    else:
        return None


def get_fb_cover_url(page_id):
    url = f"{ FB_API_ROOT }/{ page_id }?fields=cover&{ FB_TOKEN }"
    response = http_get(url)
    cover_url = response.json()['cover']['source']
    return cover_url

def content_size_match(url, excpected_size):
    response = requests.head(url)
    return response.headers['content-length'] == excpected_size

def skip_empty_lines(text):
    for line in text:
        line = line.strip()
        if line:
            yield line

def ocr_image(image, langHint="hu"):
    img_request = {"requests": [{
        "image": {"content": b64encode(image.getvalue()).decode('ascii')},
        "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
        "imageContext": {"languageHints": [langHint]}
    }]}
    response = requests.post(VISION_API_ROOT, json=img_request,
                             params={'key': config.GCP_API_KEY},
                             headers={'Content-Type': 'application/json'},
                             timeout=10)
    if response.status_code != 200 or response.json().get('error'):
        print("[ebedke] Google OCR error", response.text)
        return ""
    return response.json()['responses'][0]['textAnnotations'][0]['description']

def normalize_menu(text):
    if len(text.strip()) < 16:
        return ""
    if any(word in text.lower() for word in ("zárva", "ünnep", "nincs menü")):
        return ""
    return text.strip()

def workday(date):
    datestr = date.strftime("%Y-%m-%d")
    extra_workdays_2018 = [
        "2018-03-10", "2018-04-21", "2018-10-13", "2018-11-10", "2018-12-01",
        "2018-12-15"
    ]

    if datestr in extra_workdays_2018:
        return True

    holidays_2018 = [
        "2018-01-01", "2018-03-15", "2018-03-16", "2018-03-30", "2018-04-01",
        "2018-04-02", "2018-04-30", "2018-05-01", "2018-05-20", "2018-05-21",
        "2018-08-20", "2018-10-22", "2018-10-23", "2018-11-01", "2018-11-02",
        "2018-12-24", "2018-12-25", "2018-12-26", "2018-12-31"
    ]

    if datestr in holidays_2018:
        return False

    return date.weekday() < 5

def on_workdays(func):
    def wrapper(*args, **kwargs):
        if not workday(args[0]):
            return ""
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
            drop = True
        elif not drop:
            yield i

def remove_accents(text):
    nfkd = unicodedata.normalize('NFKD', text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))
