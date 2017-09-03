from datetime import datetime as dt
from provider.utils import get_dom


URL = "http://www.golvonalbisztro.hu/heti-menuajanlat.html"

def getMenu(today):
    day = today.weekday()
    weekdays = {
        0: "HÉTFŐ",
        1: "KEDD",
        2: "SZERDA",
        3: "CSÜTÖRTÖK",
        4: "PÉNTEK"
    }
    try:
        dom = get_dom(URL)
        menu = dom.xpath(f'//div[@class="fck"]//h3[contains(node(), "{ weekdays[day] }")]/'
                         'following-sibling::p[position() >= 1 and position() < 3]')
        menu = '<br>'.join(p.text for p in menu)
    except:
        menu = ''

    return {
        'name': 'Gólvonal',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(dt.today()))
