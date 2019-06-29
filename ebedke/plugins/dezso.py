from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://dezsoba.hu/hu/heti-menue"

@on_workdays
def getMenu(today):
    day = today.weekday()
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//div[@class="sppb-menu-text"]')
    if len(menu) < 4:
        menu = []
    else:
        menu = menu[day].xpath("text()")

    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Dezső bá',
    id='db',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(minutes=20),
    cards=[],
    groups=["corvin"],
    coord=(47.486810, 19.076372)
)
