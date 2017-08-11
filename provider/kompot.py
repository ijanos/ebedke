import json
import urllib.parse
import urllib.request
from datetime import datetime

import config

KOMPOT_FB_PAGE = "https://www.facebook.com/KompotBisztro/"
FB_ID = "405687736167829"

def getMenu(today):
    params = urllib.parse.urlencode({"access_token": config.FB_ACCESS_TOKEN})
    url = f"https://graph.facebook.com/v2.10/{FB_ID}/posts?{params}"

    resp = urllib.request.urlopen(url).read()
    posts = json.loads(resp)
    menu = next((p for p in posts['data']
                 if datetime.strptime(p['created_time'], '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
                 and "menü" in p['message']), {'message': '-'})

    menu = ' '.join(filter(lambda s: s[0] is not '#',  menu['message'].split()))
    menu = menu.replace("A:", "<br>A:")
    menu = menu.replace("B:", "<br>B:")

    return {
        'name': 'Kompót',
        'url': KOMPOT_FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    getMenu(datetime.today())
