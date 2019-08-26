from typing import List
from io import BytesIO
from datetime import timedelta
from datetime import datetime
from PIL import Image
from ebedke.pluginmanager import EbedkePlugin
from ebedke.utils.utils import ocr_image, on_workdays
from ebedke.utils.http import get_fresh_image
from ebedke.utils.text import pattern_slice
from ebedke.utils.http import get_dom
from ebedke.utils.date import days_lower

URL_ROOT = "http://bonnierestro.hu"
URL = f"{URL_ROOT}/hu/napimenu/"

@on_workdays
def get_menu(today: datetime) -> List[str]:
    menu: List[str] = []
    dom = get_dom(URL)
    menu_img = dom.xpath("/html/body//img[contains(@src, 'napi')]")
    img_src = menu_img.pop().get("src")
    img_url = f"{URL_ROOT}{img_src}"
    image = get_fresh_image(img_url, today - timedelta(days=6))
    if image:
        img = Image.open(BytesIO(image)).convert('L')
        f = BytesIO()
        img.save(f, format="png", optimize=True, compress_level=9)
        text = ocr_image(f)
        if text:
            menu = text.splitlines()
    menu = pattern_slice(menu, [days_lower[today.weekday()]], days_lower + ["menü ár", "a menü mellé", "ajándék"])
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='Bonnie',
    id='boni',
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.492182, 19.056561)
)
