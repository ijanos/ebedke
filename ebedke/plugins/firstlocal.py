from datetime import timedelta
from ebedke.utils.date import on_workdays
from ebedke.pluginmanager import EbedkePlugin

FB_URL = "https://www.facebook.com/pg/FIRSTLocalCraftBeerandKitchen/posts/"

@on_workdays
def getMenu(_today):
    return []

plugin = EbedkePlugin(
    enabled=True,
    name='FIRST Local',
    id='frstl',
    url=FB_URL,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["ferenciek"],
    coord=(47.497485, 19.057512)
)
