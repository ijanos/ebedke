from datetime import timedelta
from provider.utils import get_dom, on_workdays, months_hu_capitalized

URL = "http://vigvarju.vakvarju.com/deli-menu/"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = f"{months_hu_capitalized[today.month - 1]} {today.day:02}"
    menu = dom.xpath(f'/html/body//p[contains(preceding-sibling::p, "{date}")]/text()')
    menu = list(dish.strip() for dish in menu)

    return menu

menu = {
    'name': 'Víg Varjú',
    'id': 'vv',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': []
}
