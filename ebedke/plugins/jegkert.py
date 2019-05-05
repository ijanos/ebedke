from datetime import timedelta
from ebedke.utils.utils import on_workdays, skip_empty_lines
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://www.jegkert.hu/napiebedmenu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = today.strftime("%Y-%m-%d")
    menu = dom.xpath(f'/html/body//div[@id="NapiEbedMenu"]//tr[.//div[contains(text(), "{ date }")]]/td[position()=2 or position()=3]//text()')
    if menu:
        menu = list(skip_empty_lines(menu))
    else:
        menu = []

    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Jégkert',
    id='jk',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    groups=["szell"]
)
