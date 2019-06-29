from datetime import datetime, timedelta
from ebedke.utils.utils import days_lower, skip_empty_lines, on_workdays
from ebedke.utils import facebook
from ebedke.utils.text import pattern_slice
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/HomeFieldPub/"
FB_ID = "190139087785846"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and sum(day in post['message'].lower() for day in days_lower) >= 2
    menu = facebook.get_filtered_post(FB_ID, menu_filter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower + ["tel:", "797"])
    return list(skip_empty_lines(menu))


plugin = EbedkePlugin(
    enabled=True,
    name='HomeField Pub',
    id='hfp',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    groups=["ferenciek"],
    coord=(47.494157, 19.051109)
)
