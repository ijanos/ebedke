from datetime import timedelta

from provider.utils import get_dom, on_workdays

URL = "https://www.wasabi.hu/szolgaltatas/napimenu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL, force_utf8=True)
    weekday = today.isoweekday()
    items = dom.xpath(f'//blockquote[{weekday}]/span/strong/text()', smart_string=False)
    menu = "<br>".join(line.strip() for line in items[1:])
    return menu

menu = {
    'name': 'Wasabi',
    'id': 'wasabi',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['szep', 'erzs']
}
