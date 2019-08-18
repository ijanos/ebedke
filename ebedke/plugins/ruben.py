import re
from datetime import timedelta, date
from ebedke.utils.utils import on_workdays
from ebedke.utils.date import parse_hungarian_month, days_lower
from ebedke.utils.http import get_dom
from ebedke.utils.text import pattern_slice
from ebedke.pluginmanager import EbedkePlugin

URL = "http://www.rubenrestaurant.hu/napimenu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    greeting = dom.xpath('/html/body//h3//text()')
    date_match = re.search(r"(\d{4}). (\w+) (\d+)", " ".join(greeting))
    if date_match:
        year = int(date_match.group(1))
        month = parse_hungarian_month(date_match.group(2))
        day = int(date_match.group(3))
        menu_date = date(year, month, day)
    else:
        return []
    if menu_date <= today.date() < menu_date + timedelta(days=7):
        menu = dom.xpath('/html/body//div[@id="menulist"]//text()')
        menu = pattern_slice(menu, [days_lower[today.weekday()]], days_lower)
        menu = [line.replace("•", "") for line in menu]
        return menu
    return []


plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='Ruben Étterem',
    id='rbn',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.493062, 19.059958)
)
