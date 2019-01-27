from datetime import timedelta
import re

from provider.utils import get_dom, on_workdays, days_upper

URL = "https://www.wasabi.hu/szolgaltatas/napimenu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL, force_utf8=True)
    weekday = today.isoweekday()
    items = dom.xpath(f"//blockquote[{weekday}]//text()")[1:]
    for stopword in ["LEVES", "FŐÉTEL", "DESSZERT", "ELŐÉTEL", ":"] + days_upper:
        items = [re.sub(f'({stopword}):? ?', '', i).strip() for i in items]
    menu = list(line.strip() for line in items if line)
    return menu

menu = {
    'name': 'Wasabi',
    'id': 'wasabi',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['szep', 'erzs']
}
