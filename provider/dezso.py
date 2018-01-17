from datetime import datetime as dt
from datetime import timedelta
from provider.utils import get_dom, on_workdays

URL = "http://dezsoba.hu/hu/heti-menue"

@on_workdays
def getMenu(today):
    day = today.weekday()
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//div[@class="sppb-menu-text"]')
    menu = '<br>'.join(menu[day].xpath("text()"))

    return menu

menu = {
    'name': 'Dezső bá',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(minutes=26)
}

if __name__ == "__main__":
    print(getMenu(dt.today()))
