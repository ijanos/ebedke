from datetime import datetime as dt
from provider.utils import get_dom


URL = "http://www.golvonalbisztro.hu/heti-menuajanlat.html"

def getMenu(today):
    day = today.weekday() + 1
    try:
        dom = get_dom(URL)
        menu = dom.xpath(f'//div[@class="fck"]//h3[{ day }]/'
                         'following-sibling::p[position() >= 1 and position() < 3]/text()')
        menu = [m.strip() for m in menu if m.strip()]
        menu = '<br>'.join(menu)
    except:
        menu = ''

    return {
        'name': 'Gólvonal',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(dt.today()))
