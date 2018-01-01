from datetime import datetime as dt, timedelta
from provider.utils import get_dom

URL = "http://cafeintenzo.hu/#hetimenu"

def getMenu(today):
    day = today.weekday()
    menu = ''
    try:
        if day < 5:
            dom = get_dom(URL)
            menu = dom.xpath('//section[@id="hetimenu"]//div[contains(@class, "text_box")]')
            menu = '<br>'.join(menu[day].xpath("p/text()"))
    except:
        pass

    return menu

menu = {
    'name': 'Intenzo',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=1)
}

if __name__ == "__main__":
    print(getMenu(dt.today()))
