import re
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image

from ebedke.utils.date import on_workdays
from ebedke.utils.utils import ocr_image
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/PodiumBistroAndClub/posts/"
FB_ID = "265810157626258"


def menu_filter(post, today):
    is_this_week = datetime.strptime(post['created_time'],
                                     '%Y-%m-%dT%H:%M:%S%z').date() >= today.date() - timedelta(days=7)
    text = post['message'].lower()
    return is_this_week and ("menu" in text or "menü" in text)

@on_workdays
def get_menu(today):
    image = facebook.get_post_attached_image(FB_ID, lambda post: menu_filter(post, today))
    if not image:
        return []
    image = Image.open(BytesIO(image)).convert('L')
    f = BytesIO()
    image.save(f, format="png", optimize=True)
    raw_menu = ocr_image(f).splitlines()
    if not raw_menu:
        return []

    menu = []
    for i in raw_menu:
        m = re.match(r'(.*?)\s+(\d+,-)', i)
        if m:
            menu.append(m.groups()[0])
    return menu


plugin = EbedkePlugin(
    enabled=True,
    groups=["szepvolgyi"],
    name='Pódium Bistro & Club',
    id='podium',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.529662, 19.038243)
)
