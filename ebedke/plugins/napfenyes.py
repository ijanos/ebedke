from typing import List
from datetime import timedelta, datetime
from ebedke.pluginmanager import EbedkePlugin
from ebedke.utils.http import get_dom
from ebedke.utils.text import pattern_slice, skip_empty_lines
from ebedke.utils.date import months_hu_lower

URL = "https://napfenyesetterem.hu/vegan-vegetarianus-napi-ajanlatok/"


def getMenu(today: datetime) -> List[str]:
    dom = get_dom(URL)
    tables = dom.xpath('/html/body//table[@class="napi_table"]')
    menu: List[str] = []
    for table in tables:
        datetextlist = table.xpath("tr[@class='datum_tr']//text()")
        menutextlist = table.xpath("tr[not(@class)]/td[@class='napi_td1']//text()")
        menu.extend(datetextlist)
        menu.extend(menutextlist)

    today_string = f"{months_hu_lower[today.month - 1]} {today.day}."
    menu = pattern_slice(menu, [today_string], [f"{today.year}", f"{today.year + 1}"])
    menu = skip_empty_lines(menu, ["séfünk ajánlata"])
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='Napfényes étterem',
    id='npf',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    coord=(47.492352, 19.055191)
)
