import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

import config


URL = "https://www.facebook.com/PortumCorvin/posts/"
FB_ID = "728866253985071"

def getMenu(today):
    params = urllib.parse.urlencode({"access_token": config.FB_ACCESS_TOKEN})
    url = f"https://graph.facebook.com/v2.10/{FB_ID}/posts?{params}"

    resp = urllib.request.urlopen(url).read()
    posts = json.loads(resp)
    parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
    menu = next((p for p in posts['data']
                 if parse_date(p['created_time']) > today.date() - timedelta(days=7)
                 and "menü" in p['message'].lower()),
                {'message': ''})

    menu = menu['message']
    if "Előételek:" in menu:
        menu = menu.split("Előételek:")[1]
    menu = '<br>'.join((i for i in menu.split('\n') if i))

    return {
        'name': 'Portum',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
