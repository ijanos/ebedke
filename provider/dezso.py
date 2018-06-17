from datetime import timedelta
from provider.utils import get_dom, on_workdays

URL = "http://dezsoba.hu/hu/heti-menue"

@on_workdays
def getMenu(today):
    day = today.weekday()
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//div[@class="sppb-menu-text"]')
    if len(menu) < 4:
        menu = ''
    else:
        menu = '<br>'.join(menu[day].xpath("text()"))

    return menu

menu = {
    'name': 'Dezső bá',
    'id': 'db',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(minutes=26),
    'cards': ['erzs']
}
