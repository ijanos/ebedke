from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://mangacowboy.hu/"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = today.strftime("%Y. %m. %d.")
    menu = dom.xpath(f'//section[@id="weekly_menu"]/ul/li[.//time[contains(text(), "{ date }")]]'
                     '//div[@class="weeklyMenuPreview-content"]')
    if menu:
        menu = list(menu[0].xpath("./p/text()"))
    else:
        menu = []

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Manga Cowboy',
    id='mc',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=['szep', 'erzs']
)
