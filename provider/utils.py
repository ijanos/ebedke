from  urllib.parse import urlencode
from base64 import b64encode
import requests
from lxml import html
import config

if config.PERSISTENT_CACHE:
    import requests_cache
    from datetime import timedelta
    requests_cache.install_cache('debug_cache', expire_after=timedelta(days=1))


FB_TOKEN = urlencode({"access_token": config.FB_ACCESS_TOKEN})
FB_API_ROOT = "https://graph.facebook.com/v2.11"

HEADERS = {
    'User-Agent': config.USER_AGENT,
}


days_lower = ["hétfő", "kedd", "szerda", "csütörtök", "péntek"]


def get_dom(URL):
    response = requests.get(URL, HEADERS)
    return html.fromstring(response.text)

def get_filtered_fb_post(page_id, post_filter):
    url = f"{ FB_API_ROOT }/{ page_id }/posts?{ FB_TOKEN }"
    response = requests.get(url)
    posts = response.json()['data']
    for post in posts:
        if "message" in post and post_filter(post):
            return post["message"]
    return ""

def get_post_attachments(post_id):
    url = f"{ FB_API_ROOT }/{ post_id }/attachments?{ FB_TOKEN }"
    return requests.get(url).json()

def get_fb_cover_url(page_id):
    url = f"{ FB_API_ROOT }/{ page_id }?fields=cover&{ FB_TOKEN }"
    response = requests.get(url)
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
