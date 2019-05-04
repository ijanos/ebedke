from datetime import timedelta
from ebedke.utils.utils import get_dom, on_workdays, pattern_slice, days_lower
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
    cards=[]
)
