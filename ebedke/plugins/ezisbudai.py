from datetime import datetime, timedelta
from utils.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays, pattern_slice
from plugin import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/ezisbudai/posts"
FB_ID = "291700778001319"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and sum(day in post['message'].lower() for day in days_lower) >= 2
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower + ["wolt", "ez is budai", "nyitva", "rendelj"], inclusive=True)
    menu = skip_empty_lines(menu)
    return list(menu)


plugin = EbedkePlugin(
    enabled=True,
    name='EZ is BUDAI',
    id='eb',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    groups=["szell"]
)
