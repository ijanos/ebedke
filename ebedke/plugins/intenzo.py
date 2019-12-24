from datetime import timedelta
from ebedke.utils.date import on_workdays
from ebedke.utils.http import get_dom
from ebedke.utils.text import skip_empty_lines
from ebedke.pluginmanager import EbedkePlugin

URL = "http://cafeintenzo.hu/#hetimenu"

@on_workdays
def getMenu(today):
    day = today.weekday()
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//section[@id="hetimenu"]//div[contains(@class, "text_box")]')
    ptags = menu[day].xpath("p")
    menu = (p.text_content() for p in ptags)
    menu = skip_empty_lines(menu, dropwords=["menü ára"])

    return menu

plugin = EbedkePlugin(
    enabled=True,
    name='Intenzo',
    id='iz',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(minutes=45),
    cards=['szep', 'erzs'],
    groups=["corvin"],
    coord=(47.488949, 19.061771)
)
