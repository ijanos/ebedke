from datetime import timedelta
from ebedke.utils.date import days_lower
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.utils.text import pattern_slice
from ebedke.pluginmanager import EbedkePlugin


URL = "http://www.melodin.hu/stoczek-melodin-menza"


@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    now = f"{today.year}-{today.month:02}-{today.day:02}"

    menu = []
    for menu_type in (20, 21):
        menu_text = dom.xpath(f'/html/body//div[@class="menu-type-{menu_type}"]//div[@class="row menu"]//*[not(self::a)]/text()')
        for line in pattern_slice(menu_text, [now], days_lower + [str(today.year), str(today.year+1)]):
            menu.extend(line.split(","))

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["moricz"],
    name='Stoczek menza',
    id='stczk',
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.479195, 19.055376)
)
