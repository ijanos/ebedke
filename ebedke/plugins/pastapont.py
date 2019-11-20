from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/pastapont/posts/"
FB_ID = "362402020524227"

@on_workdays
def getMenu(_today):
    return []

plugin = EbedkePlugin(
    enabled=True,
    name='Pasta.',
    id='psta',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    groups=["ferenciek"],
    coord=(47.489606, 19.061087)
)
