import urllib.request
from io import BytesIO
from base64 import b64encode
from datetime import datetime

from PIL import Image

from provider.utils import create_img


WIDTH = 513
HEIGHT = 284


URL = "http://www.10minutes.hu/"
IMG_PATH = "images/home_1_06.png"

def getMenu(today):
    with urllib.request.urlopen(URL + IMG_PATH) as response:
        lastmod = response.getheader("Last-Modified")
        if today.date() == datetime.strptime(lastmod, '%a, %d %b %Y %H:%M:%S %Z').date():
            r = response.read()
            menu_img = Image.open(BytesIO(r))

            a_menu_box = (234, 54, 234 + WIDTH, 54 + HEIGHT)
            b_menu_box = (234, 452, 234 + WIDTH, 452 + HEIGHT)

            amenu = menu_img.crop(a_menu_box)
            bmenu = menu_img.crop(b_menu_box)

            new_im = Image.new('L', (WIDTH * 2, HEIGHT))
            new_im.paste(amenu, (0, 0))
            new_im.paste(bmenu, (WIDTH, 0))

            new_im = new_im.point(lambda i: i < 100 and 255)
            new_im = new_im.convert('1')
            zoom = 0.6
            new_im = new_im.resize((int(WIDTH * 2 * zoom), int(HEIGHT * zoom)), Image.ANTIALIAS)

            f = BytesIO()
            new_im.save(f, format="png", optimize=True, compress_level=9, bits=1)
            menu = create_img(f)
        else:
            menu = ""

        return {
            'name': '10 minutes',
            'url' : URL,
            'menu': menu
        }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
