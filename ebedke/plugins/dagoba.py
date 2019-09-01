from datetime import datetime, timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/Dagoba-bisztró-1742309292469507/posts"
FB_ID = "1742309292469507"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_heuristic = lambda msg: msg.count('-') + msg.count(':') + msg.count('+') >= 3
    menu_filter = lambda post: is_today(post['created_time']) and menu_heuristic(post['message'])
    menu = facebook.get_filtered_post(FB_ID, menu_filter).splitlines()
    drop = lambda l: l.strip().endswith((':', '!', '.', ','))
    for i in (n for n in (0, -1) if menu and drop(menu[n])):
        menu.pop(i)

    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Dagoba',
    id='dg',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=23),
    cards=[],
    groups=["corvin"],
    coord=(47.486748, 19.080351)
)
