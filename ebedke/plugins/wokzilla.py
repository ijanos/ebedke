from typing import List
from io import BytesIO
from datetime import timedelta, datetime as dt
from ebedke.utils import image, http, utils, text, date
from ebedke.pluginmanager import EbedkePlugin

URL = "https://www.wokzilla.hu/weeklymenu"
API = "https://onemin-prod.herokuapp.com/api/restaurants/42"


@utils.on_workdays
def getMenu(today: dt) -> List[str]:
    out: List[str] = []
    infojson = http.get(API).json()
    weeklyimageurl = next((obj for obj in infojson["configs"] if obj["key"] == "weeklyimgurl"), None)
    parse_date = lambda d: dt.strptime(d, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    if weeklyimageurl and today.date() - timedelta(days=6) <= parse_date(weeklyimageurl["updated_at"]) <= today.date():
        img_url = weeklyimageurl["value"]
        menu_image = image.load_img(img_url)
        w, h = menu_image.size
        cropbox = (0, round(h * 0.25), w, h)
        menu_image = menu_image.crop(cropbox)
        image_bytes = BytesIO()
        menu_image.save(image_bytes, format="png", optimize=True, compress_level=9)
        menu = image.ocr_image(image_bytes.getvalue())
        out = text.pattern_slice(menu.splitlines(), [date.days_lower[today.weekday()]], date.days_lower)
    return out

plugin = EbedkePlugin(
    enabled=True,
    name='Wokzilla',
    id='wkz',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["corvin"]
)
