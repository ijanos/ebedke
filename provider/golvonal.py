from datetime import datetime as dt
from provider.utils import get_dom, days_lower


URL = "http://www.golvonalbisztro.hu/heti-menuajanlat.html"

def getMenu(today):
    day = today.weekday()
    try:
        dom = get_dom(URL)
        days = dom.xpath('//div[@class="fck"]//h3')
        for i, dayname in enumerate([h3.text_content() for h3 in days]):
            if days_lower[day] in str.lower(dayname):
                select = i + 1
        menu = dom.xpath(f'//div[@class="fck"]//h3[{ select }]/'
                         'following-sibling::p[position() >= 1 and position() < 3]//text()')
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
