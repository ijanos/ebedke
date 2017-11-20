from datetime import datetime as dt
from itertools import dropwhile, islice
from provider.utils import get_dom, days_lower, skip_empty_lines


URL = "http://www.golvonalbisztro.hu/heti-menuajanlat.html"

def getMenu(today):
    day = today.weekday()
    try:
        dom = get_dom(URL)
        menu = dom.xpath("/html/body//div[@class='fck']/*[self::h3 or self::p]//text()")
        menu = dropwhile(lambda line: days_lower[day] not in line.lower(), menu)
        menu = islice(skip_empty_lines(menu), 1, 3)
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
