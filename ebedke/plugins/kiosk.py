from datetime import timedelta
from ebedke.utils.utils import on_workdays, months_hu_capitalized
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin


URL = "https://www.kiosk-budapest.hu/"

@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    weeklymenu = dom.xpath("/html/body//div[contains(@class, 'hetimenupluginbox')]")
    clean = lambda text: '\n'.join(n.strip() for n in text)
    weeklymenu = {
        clean(day.xpath("./div[@class='datum']//text()")): clean(day.xpath("./div[@class='hetimenulist']//text()"))
        for day in weeklymenu
    }

    date = f"{months_hu_capitalized[today.month - 1]} {today.day:02}."
    return weeklymenu[date.lower()].splitlines()

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='KIOSK',
    id='kio',
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=23),
    cards=[]
)
