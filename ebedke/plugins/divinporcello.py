from datetime import timedelta
from ebedke.utils.utils import on_workdays, months_hu_capitalized
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "https://divinporcello.hu/napi-menu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    #date = f"{months_hu_capitalized[today.month - 1]} {today.day:02}"
    menu = dom.xpath("/html/body//img[contains(@src, 'heti')]/@src")

    return menu

plugin = EbedkePlugin(
    enabled=False,
    name='Divin Porcello',
    id='dp',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["ferenciek"]
)
