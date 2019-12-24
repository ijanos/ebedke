from datetime import timedelta
from ebedke.utils.date import on_workdays
from ebedke.pluginmanager import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/sonkaarcok/posts"
FB_ID = "189659631174505"

@on_workdays
def getMenu(_today):
    return []

plugin = EbedkePlugin(
    enabled=True,
    name='SonkaArcok',
    id='ska',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    groups=["ferenciek"],
    coord=(47.490826, 19.059251)
)
