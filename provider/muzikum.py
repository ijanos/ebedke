from datetime import timedelta, datetime
from provider.utils import get_dom, on_workdays


URL = "http://muzikum.hu/heti-menu/"

@on_workdays
def getMenu(today):
    day = today.weekday()
    dom = get_dom(URL)
    date = dom.xpath('//div[@class="content-right"]//h2/text()')
    date = date[0].strip().split('|')[1].strip()[:5]
    date = datetime.strptime(f'{ today.year }.{ date }', '%Y.%m.%d').date()
    if date > today.date() - timedelta(days=7):
        menu = dom.xpath('//div[@class="content-right"]//div/p[not(span)]')
        menu = menu[day].text_content().replace('\n', '<br>')
    else:
        menu = ''

    return menu

menu = {
    'name': 'Muzikum',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=8)
}
