from datetime import datetime as dt
from provider.utils import get_dom


URL = "http://verandaetterem.hu/heti-menu/"

def getMenu(today):
    day = today.weekday() + 3
    try:
        dom = get_dom(URL)
        tds = dom.xpath(f'(//div[@id="main-content"]//table)[1]//tr[position() > 0 and position() < 5]/td[{ day }]')
        menu = "<br>".join(td.text_content().strip() for td in tds)
        if "zárva" in menu.lower():
            menu = ''
    except:
        menu = ''

    return {
        'name': 'Veranda',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(dt.today()))
