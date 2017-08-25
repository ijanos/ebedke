import json
import urllib.parse
import urllib.request
from io import BytesIO
from math import floor
from base64 import b64encode
from datetime import timedelta, datetime

from PIL import Image

import config

FB_PAGE = "https://www.facebook.com/pg/gilicekonyha/posts/"
FB_ID = "910845662306901"

def cutimage(url, day):
    with urllib.request.urlopen(url) as response:
        r = response.read()
        menu_img = Image.open(BytesIO(r))

        WIDTH = 485
        HEIGHT = 125
        X = 140
        Y = 81
        Y = Y + (HEIGHT * day)
        dailybox = (X, Y, X + WIDTH, Y + HEIGHT)

        menu = menu_img.crop(dailybox)
        (menu, _, _) = menu.split()

        new_im = Image.new('L', (WIDTH, HEIGHT))
        new_im.paste(menu, (0, 0))

        new_im = new_im.point(lambda i: i > 85 and 255)
        new_im = new_im.resize((WIDTH, floor(HEIGHT * 0.55)), Image.BOX)
        new_im = new_im.convert('1')

        f = BytesIO()
        new_im.save(f, format="png", optimize=True, compress_level=9, bits=4)
        return f"<img style='width:100%;' src='data:image/png;base64,{ b64encode(f.getvalue()).decode('ascii') }'>"

def getFBMenu(today):
    day = today.weekday()
    params = urllib.parse.urlencode({"access_token": config.FB_ACCESS_TOKEN})
    url = f"https://graph.facebook.com/v2.10/{FB_ID}/posts?{params}"

    resp = urllib.request.urlopen(url).read()
    posts = json.loads(resp)
    parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
    try:
        menu = next((p for p in posts['data']
                     if "jelmagyarázat" in p['message']
                     and parse_date(p['created_time']) > today.date() - timedelta(days=7)),
                    {'message': '-'})
        url = f"https://graph.facebook.com/v2.10/{ menu['id'] }/attachments?{ params }"
        resp = urllib.request.urlopen(url).read()
        attachments = json.loads(resp)
        menu_pic_url = attachments['data'][0]['media']['image']['src']
        menu = cutimage(menu_pic_url, day)
    except:
        menu = '-'

    return menu

def getMenu(today):
    if today.weekday() < 5:
        menu = getFBMenu(today)
    else:
        menu = "-"

    return {
        'name': 'Gólya',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    from datetime import datetime
    print(getMenu(datetime.today()))
