from datetime import datetime, timedelta
from ebedke.utils.utils import on_workdays, pattern_slice
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/shakeratocaffe/posts/"
FB_ID = "151093992248397"


def fb_filter(post, today):
    created = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
    trigger_words = ["holnapi", "mai"]
    triggered = any(word in post["message"].lower() for word in trigger_words)
    yesterday = today.date() - timedelta(days=1)
    menu_posted_yesterday = created.hour >= 12 and created.date() == yesterday and triggered
    menu_posted_today = created.hour < 12 and created.date() == today.date() and triggered
    return menu_posted_today or menu_posted_yesterday


@on_workdays
def get_menu(today):
    fbfilter = lambda post: fb_filter(post, today)
    menu = facebook.get_filtered_post(FB_ID, fbfilter)
    menu = pattern_slice(menu.splitlines(), ["holnapi", "mai"], ["tomorrow", "today", "offer"])
    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Caffe Shakerato',
    id='cfs',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["ferenciek"],
    coord=(47.495109, 19.050935)
)
