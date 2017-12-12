from datetime import datetime as dt
from provider.utils import get_dom
from lxml import etree as ET

URL = "http://www.emikifozte.hu/menuk.php"

def getMenu(_):
    try:
        dom = get_dom(URL)
        menu = dom.xpath('/html/body//tr[@class="menutablasor"]/td[3]')
        menu = '<br>'.join(e.text_content().strip('(, )') for e in menu)
    except:
        menu = ''

    return {
        'name': 'Emi kifőzte',
        'url': URL,
        'menu': menu,
        'cards': {
            'bank': True,
            'szep': True,
            'bozsi': True
        }
    }

if __name__ == "__main__":
    print(getMenu(dt.today()))
