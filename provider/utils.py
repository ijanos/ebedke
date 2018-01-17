from  urllib.parse import urlencode
from base64 import b64encode
from datetime import datetime
import operator
import requests
from lxml import html
import config

if config.PERSISTENT_CACHE:
    import requests_cache
    from datetime import timedelta
    requests_cache.install_cache('debug_cache', expire_after=timedelta(days=1))


FB_TOKEN = urlencode({"access_token": config.FB_ACCESS_TOKEN})
FB_API_ROOT = "https://graph.facebook.com/v2.11"
VISION_API_ROOT = "https://vision.googleapis.com/v1/images:annotate"

HEADERS = {
    'User-Agent': config.USER_AGENT,
}

GET = lambda url: requests.get(url, HEADERS, timeout=config.REQUEST_TIMEOUT)

days_lower = ["hétfő", "kedd", "szerda", "csütörtök", "péntek", "szombat", "vasárnap"]


def get_dom(URL):
    response = GET(URL)
    return html.fromstring(response.text)

def get_fresh_image(URL, fresh_date):
    resp = requests.head(URL, timeout=config.REQUEST_TIMEOUT)
    lastmod = resp.headers['last-modified']
    lastmod = datetime.strptime(lastmod, '%a, %d %b %Y %H:%M:%S %Z').date()
    if lastmod >= fresh_date:
        return GET(URL).content
    else:
        return None

def get_filtered_fb_post(page_id, post_filter):
    url = f"{ FB_API_ROOT }/{ page_id }/posts?{ FB_TOKEN }"
    response = GET(url)
    posts = response.json()['data']
    for post in posts:
        if "message" in post and post_filter(post):
            return post["message"]
    return ""

def get_post_attachments(post_id):
    url = f"{ FB_API_ROOT }/{ post_id }/attachments?{ FB_TOKEN }"
    return GET(url).json()

def get_fb_post_attached_image(page_id, post_filter):
    payload = {
        "fields": "message,created_time,attachments{target{id}}",
        "limit": 8,
        "access_token": config.FB_ACCESS_TOKEN
    }
    response = requests.get(f"{ FB_API_ROOT }/{ page_id }/posts", params=payload)
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
        response = requests.get(f"{ FB_API_ROOT }/{ attachments_id }", params=payload)
        images = response.json()["images"]
        large_image = max(images, key=operator.itemgetter("height"))
        return GET(large_image["source"]).content
    else:
        return None


def get_fb_cover_url(page_id):
    url = f"{ FB_API_ROOT }/{ page_id }?fields=cover&{ FB_TOKEN }"
    response = GET(url)
    cover_url = response.json()['cover']['source']
    return cover_url

def create_img(filelike):
    return f"<img style='width:100%;' src='data:image/png;base64,{ b64encode(filelike.getvalue()).decode('ascii') }'>"

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
        print("Google OCR error", response.text)
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
