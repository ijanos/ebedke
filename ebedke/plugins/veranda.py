from datetime import datetime as dt, timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://verandaetterem.hu/heti-menu/"

@on_workdays
def getMenu(today):
    day = today.weekday() + 3
    dom = get_dom(URL)
    menu_date = dom.xpath('/html/body//div[@id="content-area"]/p/text()').pop()
    menu_date = dt.strptime(menu_date.split()[0], "%Y-%m-%d")
    if menu_date >= today - timedelta(days=6):
        tds = dom.xpath(f'(//div[@id="main-content"]//table)[1]//tr[position() > 0 and position() < 5]/td[{ day }]')
        menu = list(td.text_content().strip() for td in tds)
    else:
        menu = []

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Veranda',
    id='vd',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=['szep', 'erzs'],
    coord=(47.479354, 19.079752)
)
