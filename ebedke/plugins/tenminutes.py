from typing import List
from io import BytesIO
from datetime import timedelta
from PIL import Image
from ebedke.utils.utils import ocr_image, on_workdays
from ebedke.utils.http import get_fresh_image
from ebedke.pluginmanager import EbedkePlugin

URL = "http://www.10minutes.hu/"
IMG_PATH = "images/home_1_06.png"

@on_workdays
def getMenu(today):
    menu: List[str] = []
    if today.weekday() == 0:  # Monday
        yesterday = today - timedelta(days=3)
    else:
        yesterday = today - timedelta(days=1)
    yesterday = yesterday.replace(hour=12, minute=25)
    image = get_fresh_image(URL + IMG_PATH, yesterday)
    if image:
        image = Image.open(BytesIO(image))

        WIDTH, HEIGHT = 526, 171
        x, a_y, b_y = 224, 162, 549

        a_menu_box = (x, a_y, x + WIDTH, a_y + HEIGHT)
        b_menu_box = (x, b_y, x + WIDTH, b_y + HEIGHT)

        amenu = image.crop(a_menu_box)
        bmenu = image.crop(b_menu_box)

        img = Image.new('L', (WIDTH, HEIGHT * 2))
        img.paste(amenu, (0, 0))
        img.paste(bmenu, (0, HEIGHT))

        img = img.point(lambda i: i < 100 and 255)
        img = img.convert('1')

        f = BytesIO()
        img.save(f, format="png", optimize=True, compress_level=9, bits=1)
        menu = ocr_image(f)
        if menu:
            menu = menu.splitlines()
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='10 minutes',
    id='tm',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=18),
    cards=['szep', 'erzs']
)
