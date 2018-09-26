from datetime import timedelta, datetime as dt
from provider.utils import get_dom, skip_empty_lines, on_workdays, days_lower, pattern_slice


URL = "http://www.kegsormuvhaz.hu/menu-1"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    this_year = today.strftime("%Y")
    menu_date = dom.xpath(f"/html/body//div[@id='PAGES_CONTAINER']//span[contains(text(), '{this_year}')]/text()")
    menu_date = menu_date[0].split('-')[0] if len(menu_date) > 0 else -1
    if menu_date is not -1 and dt.strptime(menu_date, "%Y.%m.%d").date() > today.date() - timedelta(days=6):
        menu = list(skip_empty_lines([p.text_content() for p in dom.xpath('/html/body//div[@id="comp-jhonyf7y"]//p')]))
        if any(days_lower[today.weekday()] in line for line in menu):
            menu = '<br>'.join(pattern_slice(menu, [days_lower[today.weekday()]], days_lower, inclusive=False))
        else:
            menu = '<br>'.join(menu)
        menu.replace('\xa0', ' ')
    else:
        menu = ''

    return menu

menu = {
    'name': 'KEG',
    'id': 'kg',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=8),
    'cards': []
}
