from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils import facebook
from ebedke.utils.text import pattern_slice
from ebedke.utils.date import days_lower
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/nikadelimenu/posts"
FB_ID = "423064674555158"


def fb_filter(post, today):
    current_date = f"{today.month:02}.{today.day:02}"
    triggered = current_date in post["message"].lower()
    return triggered


@on_workdays
def get_menu(today):
    fbfilter = lambda post: fb_filter(post, today)
    menu = facebook.get_filtered_post(FB_ID, fbfilter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower + ["ár:", "11", "15", "között"])
    return [line.strip("+- ") for line in menu]


plugin = EbedkePlugin(
    enabled=True,
    name='Nika',
    id='nka',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["ferenciek"],
    coord=(47.493694, 19.058295)
)
