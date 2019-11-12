from datetime import datetime, timedelta
from ebedke.utils.utils import days_lower, on_workdays, pattern_slice
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/B33BISTRO/posts"
FB_ID = "107533123949374"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and sum(day in post['message'].lower() for day in days_lower) >= 2
    menu = facebook.get_filtered_post(FB_ID, menu_filter)
    menu = menu.replace("•", "\n")
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower + ["wolt", "ez is budai", "nyitva", "rendelj"], inclusive=True)

    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Budai 33',
    id='eb',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    groups=["szell"],
    coord=(47.508923, 19.029450)
)
