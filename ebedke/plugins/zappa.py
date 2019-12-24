from datetime import datetime, timedelta
from ebedke.utils.date import days_lower, on_workdays
from ebedke.utils.text import pattern_slice
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/zappa.bistro.caffe/posts/"
FB_ID = "333202771769"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and sum(day in post['message'].lower() for day in days_lower) >= 2
    menu = facebook.get_filtered_post(FB_ID, menu_filter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower + ["desszert"], inclusive=False)
    return list(menu)


plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Zappa',
    id='zp',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=["erzs"],
    coord=(47.490136, 19.066286)
)
