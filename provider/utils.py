import urllib.request
from base64 import b64encode
import json
from lxml import html

import config

FB_TOKEN = urllib.parse.urlencode({"access_token": config.FB_ACCESS_TOKEN})

def get_dom(URL):
    response = urllib.request.urlopen(URL)
    r = response.read()
    return html.fromstring(r)

def get_facebook_posts(page_id):
    url = f"https://graph.facebook.com/v2.10/{ page_id }/posts?{ FB_TOKEN }"
    resp = urllib.request.urlopen(url).read()
    return json.loads(resp)

def get_post_attachments(post_id):
    url = f"https://graph.facebook.com/v2.10/{ post_id }/attachments?{ FB_TOKEN }"
    resp = urllib.request.urlopen(url).read()
    return json.loads(resp)

def create_img(filelike):
    return f"<img style='width:100%;' src='data:image/png;base64,{ b64encode(filelike.getvalue()).decode('ascii') }'>"
