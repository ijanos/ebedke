from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin


URL = "https://www.marcelloetterem.hu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = f"{today.month:02}.{today.day:02}"
    menu = dom.xpath(f"/html/body//div[.//a[contains(text(), '{date}')]]/p//text()")
    menu = [m.capitalize() for m in menu[:3]]
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["moricz"],
    name='Marcello',
    id='mrc',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=["szep", "erzs"],
    coord=(47.478988, 19.050615)
)
