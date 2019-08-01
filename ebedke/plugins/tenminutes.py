from typing import List
from io import BytesIO
from datetime import timedelta
from datetime import datetime
from itertools import dropwhile
from PIL import Image
from ebedke.utils.utils import ocr_image, on_workdays
from ebedke.utils.http import get_fresh_image
from ebedke.pluginmanager import EbedkePlugin

URL = "http://www.10minutes.hu/"
IMG_PATH = "images/home_1_06.png"

@on_workdays
def getMenu(today: datetime) -> List[str]:
    menu: List[str] = []
    if today.weekday() == 0:  # Monday
        yesterday = today - timedelta(days=3)
    else:
        yesterday = today - timedelta(days=1)
    yesterday = yesterday.replace(hour=12, minute=25)
    image = get_fresh_image(URL + IMG_PATH, yesterday)
    if image:
        img = Image.open(BytesIO(image))
        img = img.point(lambda i: i < 251 and 255)
        img = img.convert('1')

        f = BytesIO()
        img.save(f, format="png", optimize=True, compress_level=9, bits=1)

        text = ocr_image(f)
        if text:
            menu = text.splitlines()
            menu = list(dropwhile(lambda line: "menü" not in line.lower(), menu))
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='10 minutes',
    id='tm',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=18),
    cards=['szep', 'erzs'],
    coord=(47.485168, 19.074526)
)
