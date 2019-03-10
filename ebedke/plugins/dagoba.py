from datetime import datetime, timedelta
from utils.utils import get_filtered_fb_post, on_workdays
from plugin import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/Dagoba-bisztró-1742309292469507/posts"
FB_ID = "1742309292469507"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_heuristic = lambda msg: msg.count(':') + msg.count('+') >= 3
    menu_filter = lambda post: is_today(post['created_time']) and menu_heuristic(post['message'])
    menu = get_filtered_fb_post(FB_ID, menu_filter).splitlines()
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
    groups=["corvin"]
)
