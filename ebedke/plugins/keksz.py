from datetime import timedelta
from ebedke.utils.date import on_workdays
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/kekszbudapest/posts/"
FB_ID = "268952226502652"

@on_workdays
def getMenu(_today):
    return []

plugin = EbedkePlugin(
    enabled=True,
    name='Keksz',
    id='kksz',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    groups=["ferenciek"],
    coord=(47.497596, 19.057130)
)
