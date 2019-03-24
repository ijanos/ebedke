from datetime import datetime, timedelta
from ebedke.utils.utils import get_filtered_fb_post, on_workdays, pattern_slice
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/shakeratocaffe/posts/"
FB_ID = "151093992248397"


def fb_filter(post, today):
    created = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
    trigger_words = ["holnapi"]
    triggered = any(word in post["message"].lower() for word in trigger_words)
    yesterday = today.date() - timedelta(days=1)
    return created.date() == yesterday and triggered


@on_workdays
def get_menu(today):
    fbfilter = lambda post: fb_filter(post, today)
    menu = get_filtered_fb_post(FB_ID, fbfilter)
    menu = pattern_slice(menu.splitlines(), ["holnapi"], ["tomorrow"])
    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Caffe Shakerato',
    id='cfs',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["ferenciek"]
)
