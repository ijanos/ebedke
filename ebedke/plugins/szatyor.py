from datetime import datetime, timedelta
from ebedke.utils.utils import on_workdays, skip_empty_lines
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/szatyorbar/posts"
FB_ID = "140232679345332"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_filter = lambda post: is_today(post['created_time']) and "menü" in post['message'].lower()
    menu = facebook.get_filtered_post(FB_ID, menu_filter).splitlines()
    menu = list(skip_empty_lines(line.strip() for line in menu if "menü" not in line.lower()))

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["moricz"],
    name='Szatyor',
    id='sz',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=23),
    cards=[],
    coord=(47.479173, 19.050786)
)
