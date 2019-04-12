from urllib.parse import urlencode
from base64 import b64encode
from datetime import datetime
from functools import partial
import operator
import pickle
import unicodedata

import requests
from lxml import html
import redis

from ebedke import config


FB_TOKEN = urlencode({"access_token": config.FB_ACCESS_TOKEN})
FB_API_ROOT = "https://graph.facebook.com/v3.1"
VISION_API_ROOT = "https://vision.googleapis.com/v1/images:annotate"


HEADERS = {
    'User-Agent': config.USER_AGENT,
}

days_lower = ["hétfő", "kedd", "szerda", "csütörtök", "péntek", "szombat", "vasárnap"]
days_lower_ascii = ["hetfo", "kedd", "szerda", "csutortok", "pentek", "szombat", "vasarnap"]
days_upper = [day.upper() for day in days_lower]

months_hu_capitalized = ["Január", "Február", "Március",
                         "Április", "Május", "Június",
                         "Július", "Augusztus", "Szeptember",
                         "Október", "November", "December"]

DEBUG_CACHE = None

def http_get(url, params=None):
    global DEBUG_CACHE

    headers = {
        'User-Agent': config.USER_AGENT,
    }
    get = partial(requests.get, headers=headers, params=params, timeout=10)

    if config.DEBUG_CACHE_HTTP:
        if not DEBUG_CACHE:
            DEBUG_CACHE = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=False)

        cached = DEBUG_CACHE.get(f"cache:{url}")
        if not cached:
            print("[ebedke] saving to redis cache\n")
            cached = get(url)
            DEBUG_CACHE.set(f"cache:{url}", pickle.dumps(cached), ex=3600)
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
    response = http_get(f"{ FB_API_ROOT }/{ page_id }/posts?fields=attachments", params=payload)
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
                             params={'key': config.GCP_API_KEY},
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
