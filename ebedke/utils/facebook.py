from urllib.parse import urlencode
import operator


from ebedke.utils import http
from ebedke import settings


FB_TOKEN = urlencode({"access_token": settings.facebook_token})
FB_API_ROOT = "https://graph.facebook.com/v3.1"


def get_filtered_post(page_id, post_filter):
    payload = {
        "limit": 10,
        "access_token": settings.facebook_token
    }
    response = http.get(f"{ FB_API_ROOT }/{ page_id }/posts", params=payload)
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
    return http.get(url).json()

def get_post_attached_image(page_id, post_filter):
    payload = {
        "fields": "message,created_time,attachments{target{id}}",
        "limit": 8,
        "access_token": settings.facebook_token
    }
    response = http.get(f"{ FB_API_ROOT }/{ page_id }/posts?fields=attachments", params=payload)
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
            "access_token": settings.facebook_token
        }
        response = http.get(f"{ FB_API_ROOT }/{ attachments_id }", params=payload)
        images = response.json()["images"]
        large_image = max(images, key=operator.itemgetter("height"))
        return http.get(large_image["source"]).content
    else:
        return None

def get_cover_url(page_id):
    url = f"{ FB_API_ROOT }/{ page_id }?fields=cover&{ FB_TOKEN }"
    response = http.get(url)
    cover_url = response.json()['cover']['source']
    return cover_url
