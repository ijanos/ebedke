from datetime import timedelta
from ebedke.utils.utils import skip_empty_lines, on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://semmiextra.hu/bartok-bela-ut-etterem#heti-menu"

@on_workdays
def getMenu(_today):
    dom = get_dom(URL)
    menu = dom.xpath("/html/body//div[@id='heti-menu']//ul[@class='dotted']/li/text()")
    menu = list(skip_empty_lines(menu))

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["moricz", "szepvolgyi"],
    name='Semmi Extra',
    id='se',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(minutes=45),
    cards=['erzs']
)
