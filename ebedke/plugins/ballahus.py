from datetime import timedelta, datetime as dt
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin


URL = "http://www.ballahus.hu/mai_menu"

@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    menu_date = dom.xpath('/html/body//span[@class="date-display-single"]//text()')
    menu_date = dt.strptime(menu_date.pop(), '%Y-%m-%d') if menu_date else None
    if today.date() == menu_date:
        menu = dom.xpath('/html/body//div[contains(@class, "mai-menu")]//td[contains(@class, "etel-leiras")]/text()')
    else:
        menu = []

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='Balla Hús',
    id='balla',
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[]
)
