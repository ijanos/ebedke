from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "https://semmiextra.hu/#menu-heti-b"

@on_workdays
def getMenu(_today):
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//div[@id="menu-heti-b"]//div[@class="row "]/div[@class="title"]/text()')
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["moricz", "szepvolgyi"],
    name='Semmi Extra',
    id='se',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(minutes=45),
    cards=['erzs'],
    coord=[(47.476981, 19.045548), (47.529319, 19.038880)]
)
