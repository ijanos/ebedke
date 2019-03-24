from datetime import timedelta
from ebedke.utils.utils import get_dom, on_workdays, skip_empty_lines
from ebedke.pluginmanager import EbedkePlugin

URL = "http://cafeintenzo.hu/#hetimenu"

@on_workdays
def getMenu(today):
    day = today.weekday()
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//section[@id="hetimenu"]//div[contains(@class, "text_box")]')
    menu = filter(lambda l: "menü ára" not in l, menu[day].xpath("p//text()"))
    menu = list(skip_empty_lines(menu))

    return menu

plugin = EbedkePlugin(
    enabled=True,
    name='Intenzo',
    id='iz',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(minutes=45),
    cards=['szep', 'erzs'],
    groups=["corvin"]
)
