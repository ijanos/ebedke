import urllib.request
from lxml import html


PQS_MENU = "http://pqs.hu/hu/etlapok?e=56"

def getMenu(today):
    day = today.weekday() + 1
    with urllib.request.urlopen(PQS_MENU) as response:
        r = response.read()
        tree = html.fromstring(r)
        menu = ""
        try:
            texts = tree.xpath('//*[@id="menu"]//tr[th[contains(text(),"enü") '
                             'or contains(text(),"őztje") '
                             'or contains(text(),"eves")]]'
                             f'/following-sibling::tr[1]/td[{ day }]/ul//text()')
            menu = ''.join(texts)
            menu = menu.replace("Választott leves", "")
            menu = menu.replace("\t", "")
            menu = '<br>'.join((i for i in menu.split('\n') if i))
        except:
            menu = '-'

        return {
            'name': 'PQS Skypark',
            'url': PQS_MENU,
            'menu': menu
        }

if __name__ == "__main__":
    from datetime import datetime
    print(getMenu(datetime.today()))
