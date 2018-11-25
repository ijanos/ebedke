from datetime import timedelta

from provider.utils import get_dom, on_workdays

URL = "http://szepvolgyi.officebistro.hu/heti-ajanlat"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    weekday = today.isoweekday()
    items = dom.xpath(f'/html/body//table//table//tr//td[{weekday}]/span/text()')
    menu = "<br>".join(line.strip() for line in items[1:])
    return menu

menu = {
    'name': 'Office Bistro',
    'id': 'officebistro',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['erzs']
}
