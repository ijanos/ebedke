from datetime import timedelta, datetime
from utils.utils import get_filtered_fb_post, days_lower, on_workdays, pattern_slice
from plugin import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/gilicekonyha/posts/"
FB_ID = "910845662306901"

@on_workdays
def get_menu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() >= today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and "jelmagyarázat" in post['message'].lower()
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower, inclusive=False)

    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Gólya',
    id='gl',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=18),
    cards=['szep'],
    groups=["corvin"]
)
