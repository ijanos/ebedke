from datetime import timedelta, datetime
from itertools import chain
from provider.utils import get_dom, on_workdays, pattern_slice, days_lower


URL = "http://bridges.hu/#heti-menu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    this_year = today.strftime("%Y")
    date = dom.xpath(f'/html/body//*[@id="heti-menu"]//p[contains(text(), "{ this_year }")]')[0].text_content().strip()[0:10]
    this_week = lambda date: datetime.strptime(date, '%Y.%m.%d').date() > today.date() - timedelta(days=6)
    if this_week(date):
        weekly_menu = dom.xpath('/html/body//section[@id="heti-menu"]//*[self::h5 or self::p]//text()')
        menu = pattern_slice(weekly_menu, [days_lower[today.weekday()]], days_lower + ['desszert'], inclusive=False)
        dessert = pattern_slice(weekly_menu, ['desszert'], [], inclusive=True)
        menu = "<br>".join(line.strip() for line in chain(menu, dessert))
    else:
        menu = ''

    return menu

menu = {
    'name': 'Bridges',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['szep']
}
