from datetime import datetime as dt, timedelta
from provider.utils import get_dom

URL = "http://cafeintenzo.hu/#hetimenu"

def getMenu(today):
    day = today.weekday()
    menu = ''
    if day < 5:
        dom = get_dom(URL)
        menu = dom.xpath('//section[@id="hetimenu"]//div[contains(@class, "text_box")]')
        menu = filter(lambda l: "menü ára" not in l, menu[day].xpath("p/text()"))
        menu = '<br>'.join(menu)
        if len(menu) < 20:
            menu = ''

    return menu

menu = {
    'name': 'Intenzo',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(minutes=25)
}

if __name__ == "__main__":
    print(getMenu(dt.today()))
