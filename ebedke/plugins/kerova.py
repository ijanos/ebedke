from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
from ebedke.utils.date import on_workdays, days_lower
from ebedke.utils.utils import ocr_image, pattern_slice
from ebedke.utils import facebook
from ebedke.utils.text import skip_empty_lines
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/kerovaetelbar/posts/"
FB_ID = "582373908553561"


@on_workdays
def get_menu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() >= today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and "heti menü" in post['message'].lower()
    image = facebook.get_post_attached_image(FB_ID, menu_filter)
    if image:
        image = Image.open(BytesIO(image)).convert('L')
        f = BytesIO()
        image.save(f, format="png", optimize=True)
        menu = ocr_image(f).splitlines()
        if not menu:
            return []

        menu = pattern_slice(menu, [days_lower[today.weekday()]], days_lower + ['desszert', "890"], inclusive=False)
        menu = skip_empty_lines(menu, dropwords=["shutt", "stock", "wow", "awesi"])
    else:
        return []

    return menu


plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Kerova',
    id='kv',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=23),
    cards=[],
    coord=(47.486746, 19.079615)
)
