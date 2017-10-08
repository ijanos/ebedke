import json
import urllib.parse
import urllib.request
from io import BytesIO
from math import floor
from datetime import timedelta, datetime

from PIL import Image, ImageEnhance

from provider.utils import get_facebook_posts, get_post_attachments, create_img

FB_PAGE = "https://www.facebook.com/pg/gilicekonyha/posts/"
FB_ID = "910845662306901"

def cutimage(url, day):
    with urllib.request.urlopen(url) as response:
        r = response.read()
        menu_img = Image.open(BytesIO(r))

        WIDTH = 370
        HEIGHT = 123
        X = 110
        Y = 67
        Y = Y + (HEIGHT * day)
        dailybox = (X, Y, X + WIDTH, Y + HEIGHT)

        menu = menu_img.crop(dailybox)

        new_im = Image.new('L', (WIDTH, HEIGHT))
        new_im.paste(menu, (0, 0))

        enhancer = ImageEnhance.Contrast(new_im)
        new_im = enhancer.enhance(0.85)

        new_im = new_im.point(lambda i: i > 90 and 255)
        new_im = new_im.resize((WIDTH, floor(HEIGHT * 0.56)), Image.BOX)
        new_im = new_im.convert('1')

        f = BytesIO()
        new_im.save(f, format="png", optimize=True, compress_level=9, bits=4)
        return create_img(f)

def getFBMenu(today):
    day = today.weekday()
    day_names = ["hétfő", "kedd", "szerda", "csütörtök", "péntek"]
    parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
    try:
        posts = get_facebook_posts(FB_ID)
        menu = next((p for p in posts['data']
                     if "jelmagyarázat" in p['message']
                     and parse_date(p['created_time']) > today.date() - timedelta(days=7)),
                    {'message': ''})
        post_parts = menu['message'].split("HETI MENÜ")
        if len(post_parts) > 1:
            weekly_menu = post_parts[1]
            menu = weekly_menu.strip().split("\n\n")[day]
            menu = menu.replace(day_names[day], '')
            menu = '<br>'.join(menu.strip().split('\n'))
        else:
            attachments = get_post_attachments(menu['id'])
            menu_pic_url = attachments['data'][0]['media']['image']['src']
            menu = cutimage(menu_pic_url, day)
    except:
        menu = ''


    return menu

def getMenu(today):
    if today.weekday() < 5:
        menu = getFBMenu(today)
    else:
        menu = ""

    return {
        'name': 'Gólya',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    from datetime import datetime
    print(getMenu(datetime.today()))
