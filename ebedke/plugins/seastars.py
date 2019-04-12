from datetime import datetime, timedelta
from ebedke.utils.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/Haiphongvietnamesekitchen/"
FB_ID = "271018510265811"

@on_workdays
def getMenu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_keywords = ["mai menü", "napi menü", "napi ebéd", "ebédmenü", "ebéd menü", days_lower[today.weekday()]]
    menu_filter = lambda post: is_today(post['created_time']) and any(word in post['message'].lower() for word in menu_keywords)
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    drop_words = ["11:00", "1590", "mindenkit", "napi ebéd","minden menü", "étlapunk", "csodás",  "foglalj", days_lower[today.weekday()]]
    menu = (line for line in menu.splitlines() if not any(word in line.lower() for word in drop_words))

    return list(skip_empty_lines(menu))

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Hai Phong Restaurant',
    id='sst',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[]
)
