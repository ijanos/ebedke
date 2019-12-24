from datetime import datetime, timedelta
from ebedke.utils.date import on_workdays
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/Finomfalat17/"
FB_ID = "270764739711603"


def fb_filter(post, today):
    created = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
    trigger_words = ["ajánlatunk", "leves"]
    triggered = any(word in post["message"].lower() for word in trigger_words)
    return created.date() == today.date() and triggered


@on_workdays
def get_menu(today):
    fbfilter = lambda post: fb_filter(post, today)
    menu = facebook.get_filtered_post(FB_ID, fbfilter)
    drop_words = ["ajánlatunk"]
    menu = filter(lambda line: not any(word in line.lower() for word in drop_words), menu.splitlines())
    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Finom Falat',
    id='fifa',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["ferenciek"],
    coord=(47.495210, 19.050876)
)
