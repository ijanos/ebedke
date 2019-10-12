import re
from typing import List
from datetime import timedelta
from datetime import date, datetime
from ebedke.pluginmanager import EbedkePlugin
from ebedke.utils.utils import on_workdays
from ebedke.utils.text import pattern_slice
from ebedke.utils.http import get_dom
from ebedke.utils.date import days_lower

URL = "http://bonnierestro.hu/heti-menue.html"

@on_workdays
def get_menu(today: datetime) -> List[str]:
    dom = get_dom(URL)
    mainbody = dom.xpath('/html/body//section[contains(@id, "mainbody")]//text()')
    soup = "".join(mainbody)
    start_date_match = re.search(r"(\d{4})\.(\d+)\.(\d+)\.", soup)

    menu = []
    if start_date_match:
        year, month, day = start_date_match.groups()
        start = date(int(year), int(month), int(day))
        if start <= today.date() <= start + timedelta(days=6):
            menu = pattern_slice(soup.splitlines(), [days_lower[today.weekday()]], days_lower + ["chef", "ajánlat"])
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='Bonnie',
    id='boni',
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.492182, 19.056561)
)
