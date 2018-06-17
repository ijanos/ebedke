import json
import urllib.parse
import urllib.request
from io import BytesIO
from base64 import b64encode
from datetime import timedelta, datetime
from PIL import Image

import config

FB_PAGE = "https://www.facebook.com/pg/500szempar/posts/"
FB_ID = "101776716528181"

# Menu image W/H ratio
MENU_RATIO = 1.41
MENU_RATIO_THRESHOLD = 0.03

# Table cell dimensions and the top left point of the table
ROW_H = 0.0248
ROW_0 = 0.1980
COL_W = 0.1465
COL_0 = 0.1597

# W/H of the output image
WIDTH = 1000
HEIGHT = 150

def cuttable(img, x, y, w, h):
    return img.crop((
        (COL_0 + COL_W * x) * img.width,
        (ROW_0 + ROW_H * y) * img.height,
        (COL_0 + COL_W * (x + w)) * img.width,
        (ROW_0 + ROW_H * (y + h)) * img.height,
    ))

def cutimage(url, day):
    with urllib.request.urlopen(url) as response:
        r = response.read()
        menu_img = Image.open(BytesIO(r))

        # Cut table cells
        menu1 = cuttable(menu_img, day,  1, 1, 6)
        menu2 = cuttable(menu_img, day,  8, 1, 6)
        menu3 = cuttable(menu_img, day, 15, 1, 6)
        menu4 = cuttable(menu_img, day, 21, 1, 3)
        weekno = cuttable(menu_img, 2, -2.1, 1, 1)

        new_im = Image.new('L', (menu1.width * 4, menu1.height), 255)

        new_im.paste(menu1, (0, 0))
        new_im.paste(menu2, (menu1.width, 0))
        new_im.paste(menu3, (menu1.width * 2, 0))
        new_im.paste(menu4, (menu1.width * 3, 0))
        new_im.paste(weekno, (menu1.width * 3, menu4.height))

        new_im = new_im.point(lambda i: i > 125 and 255)
        new_im = new_im.convert('1')
        new_im = new_im.resize((WIDTH, HEIGHT), Image.BOX)

        f = BytesIO()
        new_im.save(f, format="png", optimize=True, compress_level=9, bits=4)
        return "<img style='width:100%;' src='data:image/png;base64," + b64encode(f.getvalue()).decode('ascii') + "'>"

def getFBMenu(today):
    params = urllib.parse.urlencode({"access_token": config.FB_ACCESS_TOKEN})
    url = f"https://graph.facebook.com/v2.10/{FB_ID}/photos?type=uploaded&fields=created_time,images&{params}"
    resp = urllib.request.urlopen(url).read()
    resp = json.loads(resp)

    img_src = None
    # Best guess: let's hope that the ratio of the menu will always be around the same
    parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
    for img in resp['data']:
        if img['images']:
            ratio = int(img['images'][0]['width']) / int(img['images'][0]['height'])
            if abs(ratio - MENU_RATIO) < MENU_RATIO_THRESHOLD and parse_date(img['created_time']) > today.date() - timedelta(days=7):
                img_src = img['images'][0]['source']
                break

    if img_src is None:
        return ""

    return cutimage(img_src, today.weekday())

def getMenu(today):
    if today.weekday() < 5:
        menu = getFBMenu(today)
    else:
        menu = "Svédasztal lehetőség hétvégén"

    return {
        'name': '500 szempár',
        'id': 'ot',
        'url': FB_PAGE,
        'menu': menu
    }
