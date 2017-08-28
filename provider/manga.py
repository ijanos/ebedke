from datetime import datetime as dt
from provider.utils import get_dom


URL = "http://mangacowboy.hu/"

def getMenu(today):
    day = today.weekday()
    try:
        dom = get_dom(URL)
        menu = dom.xpath('//*[@id="weekly_menu"]//div[@class="weeklyMenuPreview-content"]')
        menu = '<br>'.join(menu[day].xpath("p/text()"))
    except:
        menu = ''

    return {'name': 'Manga',
            'url': URL,
            'menu': menu}

if __name__ == "__main__":
    print(getMenu(dt.today()))
