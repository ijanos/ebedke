from datetime import datetime, timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils import facebook
from ebedke.utils.text import skip_empty_lines
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/Nine-Tables-Corvin-255153518398246/"
FB_ID = "255153518398246"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_words = ["mai menü", "napi menü"]
    menu_filter = lambda post: is_today(post['created_time']) and any(word in post['message'].lower() for word in menu_words)
    menu = facebook.get_filtered_post(FB_ID, menu_filter)
    if menu:
        drop_words = ["#", "mai menü", "napi menü", '"', "hétvég", "590", "...", "!", "“"]
        menu = filter(lambda l: not any(word in l.lower() for word in drop_words), menu.splitlines())
        return list(skip_empty_lines(menu))

    return []

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Nine Tables',
    id='nt',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.485983, 19.074895)
)
