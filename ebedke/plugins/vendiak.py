from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils.text import pattern_slice
from ebedke.utils.http import get_dom
from ebedke.utils.date import days_lower
from ebedke.pluginmanager import EbedkePlugin

URL = "https://www.vendiaketterem.hu/"

@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    menu = dom.xpath("/html/body//div[@class='panel-heading' or @class='offer-item']//text()")
    drop_words = ["házi tea"]
    menu = filter(lambda line: not any(word in line.lower() for word in drop_words), menu)
    return pattern_slice(menu, [days_lower[today.weekday()]], days_lower)

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='Vén Diák',
    id='vend',
    url=URL,
    downloader=get_menu,
    ttl=timedelta(minutes=20),
    cards=[],
    coord=(47.490981, 19.058805)
)
