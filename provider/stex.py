from datetime import datetime, timedelta
from io import BytesIO
from itertools import islice, takewhile, dropwhile
from PIL import Image
from provider.utils import get_dom, get_fresh_image, ocr_image, skip_empty_lines, days_lower, on_workdays

URL_ROOT = "http://stexhaz.hu"
MENU_SUFFIX = "/napimenu"

@on_workdays
def get_menu(today):
    dom = get_dom(URL_ROOT + MENU_SUFFIX)
    menu_url = dom.xpath("/html/body//div[@class='art-post-body']//img/@src").pop()
    menu_url = URL_ROOT + menu_url

    date_limit = today - timedelta(days=6)
    image = get_fresh_image(menu_url, date_limit.date())
    if not image:
        return ""

    _, image, _ = Image.open(BytesIO(image)).split()
    width, height = image.size
    cropbox = (0, round(height * 0.1583), width, height - round(height * 0.12))
    image = image.crop(cropbox)

    f = BytesIO()
    image.save(f, format="png", optimize=True, compress_level=9, bits=1)

    menu = ocr_image(f).splitlines()
    if not menu:
        return ""

    menu = islice(dropwhile(lambda l: days_lower[today.weekday()] not in l.lower(), menu), 1, None)
    menu = takewhile(lambda l: not any(day in l.lower() for day in days_lower), menu)
    menu = '<br>'.join(skip_empty_lines(menu))

    return menu

menu = {
    'name': 'Stex',
    'url' : URL_ROOT + MENU_SUFFIX,
    'get': get_menu,
    'ttl': timedelta(hours=23)
}
