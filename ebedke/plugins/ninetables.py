import re
from datetime import datetime, timedelta
from ebedke.utils.date import on_workdays
from ebedke.utils import facebook
from ebedke.utils.text import skip_empty_lines
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/Nine-Tables-Corvin-255153518398246/"
FB_ID = "255153518398246"


def fb_filter(post, today):
    created = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
    patterns = [r"mai.*menü", r"napi.*menü", r"ma.*ebéd", r"ma is.*nine tables"]
    triggered = any(re.search(pattern, post["message"].lower()) for pattern in patterns)
    posted_today = today.date() == created.date()
    return posted_today and triggered

@on_workdays
def get_menu(today):
    fbfilter = lambda post: fb_filter(post, today)
    menu = facebook.get_filtered_post(FB_ID, fbfilter)
    if menu:
        drop_words = ["#", "mai menü", "napi menü", '"', "ma is", "hétvég", "590", "...", "!", "“", "?", "tökéletes", "terasz"]
        return list(skip_empty_lines(menu.splitlines(), drop_words))

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
