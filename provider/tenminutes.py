import urllib.request
from io import BytesIO
from datetime import datetime, timedelta
from PIL import Image
from provider.utils import create_img


URL = "http://www.10minutes.hu/"
IMG_PATH = "images/home_1_06.png"

def getMenu(today):
    menu = ""
    with urllib.request.urlopen(URL + IMG_PATH) as response:
        lastmod = response.getheader("Last-Modified")
        if today.date() == datetime.strptime(lastmod, '%a, %d %b %Y %H:%M:%S %Z').date():
            r = response.read()
            menu_img = Image.open(BytesIO(r))

            WIDTH = 526
            HEIGHT = 171
            x = 224
            a_y = 162
            b_y = 549

            a_menu_box = (x, a_y, x + WIDTH, a_y + HEIGHT)
            b_menu_box = (x, b_y, x + WIDTH, b_y + HEIGHT)

            amenu = menu_img.crop(a_menu_box)
            bmenu = menu_img.crop(b_menu_box)

            new_im = Image.new('L', (WIDTH * 2, HEIGHT))
            new_im.paste(amenu, (0, 0))
            new_im.paste(bmenu, (WIDTH, 0))

            zoom = 0.6
            new_im = new_im.resize((int(WIDTH * 2 * zoom), int(HEIGHT * zoom)), Image.ANTIALIAS)

            new_im = new_im.point(lambda i: i < 100 and 255)
            new_im = new_im.convert('1')

            f = BytesIO()
            new_im.save(f, format="png", optimize=True, compress_level=9, bits=1)
            menu = create_img(f)

    return menu

menu = {
    'name': '10 minutes',
    'url' : URL,
    'get': getMenu,
    'ttl': timedelta(hours=4)
}

if __name__ == "__main__":
    print(getMenu(datetime.today()))
