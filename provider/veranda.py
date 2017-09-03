from datetime import datetime as dt
from provider.utils import get_dom


URL = "http://verandaetterem.hu/"

def getMenu(today):
    day = today.weekday() + 2
    try:
        dom = get_dom(URL)
        tds = dom.xpath(f'(//div[@id="main-content"]//table)[1]//tr[position() > 1 and position() < 6]/td[{ day }]')
        menu = "<br>".join(td.text_content().strip() for td in tds)
    except:
        menu = '-'

    return {
        'name': 'Veranda',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(dt.today()))
