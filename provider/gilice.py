import json
import urllib.parse
import urllib.request
from io import BytesIO
from math import floor
from base64 import b64encode

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

        new_im = Image.new('L', (WIDTH, HEIGHT))
        new_im.paste(menu, (0, 0))

        new_im = new_im.point(lambda i: i > 85 and 255)
        new_im = new_im.convert('1')
        new_im = new_im.resize((WIDTH, floor(HEIGHT * 0.61)), Image.ANTIALIAS)

        f = BytesIO()
        new_im.save(f, format="png", optimize=True, compress_level=9, bits=4)
        return "<img style='width:100%;' src='data:image/png;base64," + b64encode(f.getvalue()).decode('ascii') + "'>"

def getFBMenu(day):
    params = urllib.parse.urlencode({"access_token": config.FB_ACCESS_TOKEN})
    url = f"https://graph.facebook.com/v2.10/{FB_ID}/posts?{params}"

    resp = urllib.request.urlopen(url).read()
    posts = json.loads(resp)
    menu = next((p for p in posts['data']
                 if "jelmagyarázat" in p['message']), {'message': '-'})
    try:
        url = f"https://graph.facebook.com/v2.10/{ menu['id'] }/attachments?{ params }"
        resp = urllib.request.urlopen(url).read()
        attachments = json.loads(resp)
        menu_pic_url = attachments['data'][0]['media']['image']['src']
        menu = cutimage(menu_pic_url, day)
    except:
        menu = '-'

    return menu

def getMenu(today):
    day = today.weekday()
    if day < 5:
        menu = getFBMenu(day)
    else:
        menu = "-"

    return {
        'name': 'Gólya',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    from datetime import datetime
    getMenu(datetime.today())
