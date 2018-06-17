from datetime import datetime as dt, timedelta
from provider.utils import get_dom, on_workdays, skip_empty_lines

URL = "http://cafeintenzo.hu/#hetimenu"

@on_workdays
def getMenu(today):
    day = today.weekday()
    dom = get_dom(URL)
    menu = dom.xpath('//section[@id="hetimenu"]//div[contains(@class, "text_box")]')
    menu = filter(lambda l: "menü ára" not in l, menu[day].xpath("p/text()"))
    menu = '<br>'.join(skip_empty_lines(menu))

    return menu

menu = {
    'name': 'Intenzo',
    'id': 'iz',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(minutes=45),
    'cards': ['szep', 'erzs']
}
