from datetime import datetime, timedelta
from utils.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays
from plugin import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/Seastarsrestaurant/posts/"
FB_ID = "271018510265811"

@on_workdays
def getMenu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_keywords = ["napi menü", days_lower[today.weekday()]]

    menu_filter = lambda post: is_today(post['created_time']) and any(word in post['message'].lower() for word in menu_keywords)
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = ''.join(char for char in menu if ord(char) < 500)
    drop_words = ["mindenkit", "minden menü", "étlapunk", "csodás", days_lower[today.weekday()]]
    menu = (line for line in menu.splitlines() if not any(word in line.lower() for word in drop_words))

    return list(skip_empty_lines(menu))

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Seastars',
    id='sst',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[]
)
