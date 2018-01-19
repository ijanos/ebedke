from datetime import datetime as dt, timedelta
from provider.utils import get_dom, on_workdays

PQS_MENU = "http://pqs.hu/hu/etlapok?e=56"

@on_workdays
def getMenu(today):
    today = today.strftime("%Y-%m-%d")
    dom = get_dom(PQS_MENU)
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
    menu = '<br>'.join((i for i in menu.splitlines() if i))

    return menu

menu = {
    'name': 'PQS Skypark',
    'url': PQS_MENU,
    'get': getMenu,
    'ttl': timedelta(hours=6)
}

if __name__ == "__main__":
    print(getMenu(dt.today()))
