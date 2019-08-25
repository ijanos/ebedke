from datetime import datetime, timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils.date import days_lower
from ebedke.utils.text import pattern_slice
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/bartokgastropub/posts"
FB_ID = "371331030122672"

def fb_filter(post, today):
    created = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
    trigger_words = ["napi menü", "ebéd menü"]
    triggered = any(word in post["message"].lower() for word in trigger_words)
    this_week = today.date() - timedelta(days=6) < created.date() <= today.date()
    return this_week and triggered

@on_workdays
def get_menu(today):
    fbfilter = lambda post: fb_filter(post, today)
    menu = facebook.get_filtered_post(FB_ID, fbfilter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower)
    return menu

plugin = EbedkePlugin(
    enabled=True,
    name='Bartok',
    id='brtk',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["moricz"],
    coord=(47.482268, 19.052530)
)
