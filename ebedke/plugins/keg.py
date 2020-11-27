from datetime import timedelta, datetime as dt
from ebedke.utils.date import on_workdays, days_lower
from ebedke.utils.text import pattern_slice, skip_empty_lines
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://www.kegsormuvhaz.hu/menu-1"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    this_year = today.strftime("%Y")
    menu_date = dom.xpath(f"/html/body//span[contains(text(), '{this_year}')]/text()")
    menu_date = menu_date[0].split('-')[0] if menu_date else -1
    if menu_date != -1 and dt.strptime(menu_date, "%Y.%m.%d").date() > today.date() - timedelta(days=6):
        menu = list(skip_empty_lines([p.text_content() for p in dom.xpath('/html/body//div[@id="comp-jhonyf7y"]//p')]))
        if any(days_lower[today.weekday()] in line for line in menu):
            menu = list(pattern_slice(menu, [days_lower[today.weekday()]], days_lower, inclusive=False))
        else:
            menu = list(menu)
        menu = [item.replace('\xa0', ' ') for item in menu]
    else:
        menu = []

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["moricz"],
    name='KEG',
    id='kg',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=8),
    cards=[],
    coord=(47.482165, 19.052041)
)
