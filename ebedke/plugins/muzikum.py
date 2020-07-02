import re
from datetime import timedelta, date, datetime
from typing import List

from ebedke.utils.date import on_workdays, days_lower
from ebedke.utils.text import pattern_slice
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://muzikum.hu/heti-menu/"

@on_workdays
def getMenu(today: datetime) -> List[str]:
    dom = get_dom(URL)
    page_content = dom.xpath('//div[@class="content-right"]//text()')
    soup = "".join(page_content)
    start_date_match = re.search(r"(\d{4})\.(\d+)\.(\d+)", soup)

    menu: List[str] = []
    if start_date_match:
        year, month, day = start_date_match.groups()
        start = date(int(year), int(month), int(day))
        if start <= today.date() <= start + timedelta(days=6):
            menu = dom.xpath('/html/body//div[@class="content-right"]//*[not(self::em)]/text()')
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
