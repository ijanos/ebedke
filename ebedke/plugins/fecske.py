import re
from typing import List
from datetime import timedelta, date, datetime
from ebedke.utils.date import parse_hungarian_month
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin


URL = "http://www.fecskepresszo.com/heti-menu"

@on_workdays
def get_menu(today: datetime) -> List[str]:
    dom = get_dom(URL, force_utf8=True)
    menu_date = " ".join(txt.strip() for txt in dom.xpath('/html/body//div[@id="hetimenu_idopont"]//text()'))
    date_match = re.search(r"(\w+)\s(\d+)\W+(\w+)\s(\d+)", menu_date)
    if date_match:
        m1, d1, m2, d2 = date_match.groups()
        month1 = parse_hungarian_month(m1)
        month2 = parse_hungarian_month(m2)
        year1 = today.year
        year2 = today.year
        if month2 < month1:
            if today.month == month2:
                year1 = today.year - 1
            year2 = year1 + 1
        menu_start = date(year1, month1, int(d1))
        menu_end = date(year2, month2, int(d2))
        if menu_start <= today.date() <= menu_end:
            menu: List[str] = dom.xpath('/html/body//div[@id="hetimenu_menu"]//span[@class="definition"]//text()')
            return menu

    return []

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Fecske presszó',
    id='fecske',
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.489578, 19.064336)
)
