from datetime import datetime as dt
from provider.utils import get_dom

PQS_MENU = "http://pqs.hu/hu/etlapok?e=56"

def getMenu(today):
    day = today.weekday() + 1
    try:
        dom = get_dom(PQS_MENU)
        texts = dom.xpath('//*[@id="menu"]//tr[th[contains(text(),"enü") '
                          'or contains(text(),"őztje") '
                          'or contains(text(),"eves")]]'
                         f'/following-sibling::tr[1]/td[{ day }]/ul//text()')
        menu = ''.join(texts)
        menu = menu.replace("Választott leves", "")
        menu = menu.replace("\t", "")
        menu = '<br>'.join((i for i in menu.split('\n') if i))
    except:
        menu = ''

    return {
        'name': 'PQS Skypark',
        'url': PQS_MENU,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(dt.today()))
