from datetime import datetime as dt
from provider.utils import get_dom

URL = "http://dezsoba.hu/hu/heti-menue"

def getMenu(today):
    day = today.weekday()
    try:
        dom = get_dom(URL)
        menu = dom.xpath('//div[@class="sppb-menu-text"]')
        menu = '<br>'.join(menu[day].xpath("text()"))
    except:
        menu = ''

    return {
        'name': 'Dezső bá',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(dt.today()))
