from datetime import timedelta
from utils.utils import get_dom, on_workdays, skip_empty_lines
from plugin import EbedkePlugin

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
