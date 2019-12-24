from datetime import timedelta
from ebedke.utils.date import on_workdays
from ebedke.utils.text import pattern_slice
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin


URL = "https://www.marcelloetterem.hu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = f"{today.month:02}.{today.day:02}"
    page_text = dom.xpath(f"/html/body//div[./div[contains(.//text(), '{date}')]]//text()")
    tomorrow_date = f"{today.month:02}.{today.day + 1:02}"
    menu = pattern_slice(page_text, [date], [tomorrow_date, "menü", "szódával", "kávéval"])
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["moricz"],
    name='Marcello',
    id='mrc',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=24),
    cards=["szep", "erzs"],
    coord=(47.478988, 19.050615)
)
