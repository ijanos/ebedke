from datetime import timedelta
import re

from ebedke.utils.utils import on_workdays, days_upper
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

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


plugin = EbedkePlugin(
    enabled=True,
    groups=["szepvolgyi"],
    name='Wasabi',
    id='wasabi',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=['szep', 'erzs']
)
