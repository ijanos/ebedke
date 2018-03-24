from datetime import datetime as dt, timedelta
from provider.utils import get_dom, on_workdays


URL = "http://verandaetterem.hu/heti-menu/"

@on_workdays
def getMenu(today):
    day = today.weekday() + 3
    dom = get_dom(URL)
    tds = dom.xpath(f'(//div[@id="main-content"]//table)[1]//tr[position() > 0 and position() < 5]/td[{ day }]')
    menu = "<br>".join(td.text_content().strip() for td in tds)

    return menu

menu = {
    'name': 'Veranda',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(minutes=35),
    'cards': ['szep', 'erzs']
}
