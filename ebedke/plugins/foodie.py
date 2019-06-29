from datetime import datetime as dt, timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/Foodie-MinuteBistro-494549960697458/posts"
FB_ID = "494549960697458"

@on_workdays
def getMenu(today):
    is_today = lambda date: dt.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_filter = lambda post: is_today(post['created_time']) and "leveseink" in post['message'].lower()
    dailymenu = facebook.get_filtered_post(FB_ID, menu_filter)
    menu = [line for line in dailymenu.splitlines() if line.strip().startswith('-')]
    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Foodie',
    id='fd',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=['szep', 'erzs'],
    groups=["corvin"],
    coord=(47.485998, 19.075279)
)
