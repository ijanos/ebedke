from datetime import timedelta, datetime
from provider.utils import get_dom


URL = "http://muzikum.hu/heti-menu/"

def getMenu(today):
    day = today.weekday()
    menu = ''
    try:
        dom = get_dom(URL)
        weekly_menu = dom.xpath('//div[@class="content-right"]//p[not(span)]')
        date = dom.xpath('//div[@class="content-right"]//h2/text()')
        date = date[0].strip().split('|')[1].strip()[:5]
        date = datetime.strptime(f'{ today.year }.{ date }', '%Y.%m.%d').date()
        if date > today.date() - timedelta(days=7) and day < 5:
            menu = weekly_menu[day].text_content().replace('\n', '<br>')
            if len(menu) < 5:
                menu = ""
    except:
        pass

    return {
        'name': 'Muzikum',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
