from datetime import timedelta, datetime
from ebedke.utils.utils import on_workdays
from ebedke.utils.text import pattern_slice
from ebedke.utils.date import days_lower
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://muzikum.hu/heti-menu/"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = dom.xpath('//div[@class="content-right"]//h2/text()')
    date = date[0].strip().split('|')[1].strip()[:5]
    date = datetime.strptime(f'{ today.year }.{ date }', '%Y.%m.%d').date()
    if date > today.date() - timedelta(days=7):
        menu = dom.xpath('/html/body//div[@class="content-right"]//div/*[self::h3 or self::p]/text()')
    else:
        menu = []

    return pattern_slice(menu, [days_lower[today.weekday()]], days_lower + ["asztalfoglalás", "dolgozóknak"])


plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Muzikum',
    id='mz',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=['szep'],
    coord=(47.490255, 19.063264)
)
