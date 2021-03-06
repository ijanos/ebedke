from datetime import timedelta
from ebedke.utils.date import on_workdays, days_lower
from ebedke.utils.text import pattern_slice
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "https://vapiano.hu/etlap/mamma-mia-special/"

@on_workdays
def getMenu(today):
    dom = get_dom(URL, verify=False)
    menu = dom.xpath('/html/body//div[@class="etlap-container"]//text()')
    menu = pattern_slice(menu, [days_lower[today.weekday()]], days_lower)
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='Vapiano',
    id='vapi',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=3),
    cards=[],
    coord=(47.496696, 19.051125)
)
