from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

URL = "http://www.emikifozte.hu/menuk.php"

@on_workdays
def getMenu(_):
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//tr[@class="menutablasor"]/td[3]')
    menu = [e.text_content().strip('(, )') for e in menu]

    return menu

plugin = EbedkePlugin(
    enabled=True,
    name='Emi kifőzte',
    id='ek',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(minutes=25),
    cards=['szep', 'erzs'],
    groups=["corvin"]
)
