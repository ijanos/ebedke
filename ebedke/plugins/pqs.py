from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin

PQS_MENU = "http://pqs.hu/hu/etlapok?e=56"

@on_workdays
def getMenu(today):
    today = today.strftime("%Y-%m-%d")
    dom = get_dom(PQS_MENU)
    column = 0
    for i, th in enumerate(dom.xpath('//table[@id="menu"]/thead//th')):
        text = ''.join(th.xpath('text()'))
        if today in text:
            column = i + 1
    texts = dom.xpath('//*[@id="menu"]//tr[th[contains(text(),"enü") '
                      'or contains(text(),"őztje") '
                      'or contains(text(),"eves")]]'
                      f'/following-sibling::tr[1]/td[{ column }]/ul//text()')
    menu = ''.join(texts)
    menu = menu.replace("Választott leves", "")
    menu = menu.replace("\t", "")
    return list(i for i in menu.splitlines() if i)


plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='PQS Skypark',
    id='pq',
    url=PQS_MENU,
    downloader=getMenu,
    ttl=timedelta(hours=6),
    cards=['szep']
)
