from datetime import timedelta
from ebedke.utils.date import days_lower
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.utils.text import pattern_slice
from ebedke.pluginmanager import EbedkePlugin


URL = "http://matyaspince.eu/menu/"

@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//div/center//text()')
    now = f"{today.month:02}.{today.day:02}"
    return pattern_slice(menu, [now], days_lower + ["csoportok"])


plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='Mátyás pince',
    id='mtys',
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.491573, 19.053060)
)
