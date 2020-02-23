from datetime import timedelta
from ebedke.utils.date import on_workdays
from ebedke.pluginmanager import EbedkePlugin

WEB_URL = "https://divinporcello.hu/napi-menu"
FB_URL = "https://www.facebook.com/pg/DivinPorcelloBudapest/posts/"

@on_workdays
def getMenu(_today):
    return []

plugin = EbedkePlugin(
    enabled=True,
    name='Divin Porcello',
    id='dp',
    url=FB_URL,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["ferenciek"],
    coord=(47.494968, 19.049927)
)
