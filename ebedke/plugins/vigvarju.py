from datetime import timedelta
from ebedke.utils.date import on_workdays, months_hu_capitalized
from ebedke.utils.date import months_hu_lower
from ebedke.utils.http import get_dom
from ebedke.utils.text import pattern_slice
from ebedke.pluginmanager import EbedkePlugin

URL = "http://vigvarju.vakvarju.com/deli-menu/"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = f"{months_hu_capitalized[today.month - 1]} {today.day}"
    p_tags = dom.xpath(f'/html/body//p')
    menu = [p.text_content() for p in p_tags]
    menu = pattern_slice(menu, [date], months_hu_lower)
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='Víg Varjú',
    id='vv',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    coord=(47.496045, 19.049145)
)
