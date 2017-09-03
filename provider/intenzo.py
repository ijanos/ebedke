from datetime import datetime as dt
from provider.utils import get_dom

URL = "http://cafeintenzo.hu/#hetimenu"

def getMenu(today):
    day = today.weekday()
    try:
        dom = get_dom(URL)
        menu = dom.xpath('//*[@id="hetimenu"]//div[contains(@class, "text_box")]')
        menu = '<br>'.join(menu[day].xpath("p/text()"))
    except:
        menu = ''

    return {
        'name': 'Intenzo',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(dt.today()))
