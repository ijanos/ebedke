from datetime import timedelta, datetime
from provider.utils import get_dom, on_workdays


URL = "http://bridges.hu/#heti-menu"

@on_workdays
def getMenu(today):
    day = today.weekday() + 1
    dom = get_dom(URL)
    weekly_menu = dom.xpath('/html/body//section[@id="heti-menu"]//p')
    weekly_menu = list(filter(lambda p: len(p.text_content().strip()) > 0, weekly_menu))
    date = weekly_menu[0].text_content().strip()[0:10]
    this_week = lambda date: datetime.strptime(date, '%Y.%m.%d').date() > today.date() - timedelta(days=6)
    if this_week(date):
        menu = weekly_menu[day].text_content()
        menu = menu.replace('1.', '<br>1.')
        menu = menu.replace('2.', '<br>2.')
        menu = menu + '<br>' + weekly_menu[6].text_content()
    else:
        menu = ''

    return menu

menu = {
    'name': 'Bridges',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=8)
}

if __name__ == "__main__":
    print(getMenu(datetime.today()))
