from datetime import timedelta
from ebedke.utils.utils import on_workdays, days_lower, skip_empty_lines
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://szepvolgyi.officebistro.hu/heti-ajanlat"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    weekday = today.weekday()

    rows = iter(dom.xpath(f'/html/body//table//tr'))

    table = []
    for row in rows:
        row = [col.text_content().strip() for col in row]
        table.append(row)

    table = list(map(list, zip(*table)))

    menu = []
    for column in table:
        if days_lower[weekday] in column[0].lower():
            menu = list(skip_empty_lines(column[1:]))
            break

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["szepvolgyi"],
    name='Office Bistro',
    id='officebistro',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=['erzs']
)
