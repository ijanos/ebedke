from datetime import timedelta
import re

from provider.utils import get_dom, on_workdays

URL = "https://www.wasabi.hu/szolgaltatas/napimenu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL, force_utf8=True)
    weekday = today.isoweekday()
    items = dom.xpath(f"//blockquote[{weekday}]/span/*/text()")
    for course in ["LEVES", "FŐÉTEL", "DESSZERT", "ELŐÉTEL"]:
        items = [re.sub(f'({course}):? ?', '', i) for i in items]
    menu = "<br>".join(line.strip() for line in items if line)
    return menu

menu = {
    'name': 'Wasabi',
    'id': 'wasabi',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['szep', 'erzs']
}
