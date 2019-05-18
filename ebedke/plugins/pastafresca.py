from datetime import datetime, timedelta
from ebedke.utils.utils import on_workdays, days_lower, pattern_slice
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/Pastafresca-Buda-235959913862289/posts/"
FB_ID = "235959913862289"

@on_workdays
def get_menu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() >= today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and days_lower[today.weekday()] in post['message'].lower()
    menu = facebook.get_filtered_post(FB_ID, menu_filter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower, inclusive=True)
    menulist = []
    for line in menu:
        line = line.split(":", maxsplit=1)[1] if ':' in line else line
        menulist.append(line)

    return menulist

plugin = EbedkePlugin(
    enabled=True,
    groups=["szell"],
    name='Pasta Fresca Buda',
    id='pfr',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=23),
    cards=[]
)
