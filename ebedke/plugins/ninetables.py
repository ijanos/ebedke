from datetime import datetime, timedelta
from utils.utils import get_filtered_fb_post, on_workdays
from utils.text import skip_empty_lines
from plugin import EbedkePlugin

FB_PAGE = "https://www.facebook.com/Nine-Tables-Corvin-255153518398246/"
FB_ID = "255153518398246"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_words = ["mai menü", "napi menü"]
    menu_filter = lambda post: is_today(post['created_time']) and any(word in post['message'].lower() for word in menu_words)
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    if menu:
        drop_words = ["#", "mai menü", "napi menü", '"', "hétvég", "590", "...", "!", "“"]
        menu = filter(lambda l: not any(word in l.lower() for word in drop_words), menu.splitlines())
        return list(skip_empty_lines(menu))
    else:
        return []

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Nine Tables',
    id='nt',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[]
)
