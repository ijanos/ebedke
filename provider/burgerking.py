import urllib.request
from lxml import html

URL = "http://burgerking.hu/cikkek/friss-hirek/uj-hetkoznapi-burger-king-menu"

def getMenu(_):
    with urllib.request.urlopen(URL) as response:
        r = response.read()
        tree = html.fromstring(r)
        weeklymenu = tree.xpath('//*[@id="tabs-0"]/div[7]/div/p[5]//text()')
        weeklymenu = [item for item in weeklymenu if item.strip() is not '']
        addbr = lambda s: "<br>" + s if ':' in s else s
        menu = ' '.join([addbr(i) for i in weeklymenu])
        return {
            'name': 'Burger King',
            'url': URL,
            'menu': menu
        }

if __name__ == "__main__":
    from datetime import datetime
    print(getMenu(datetime.today()))
