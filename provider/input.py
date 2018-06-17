from datetime import datetime, timedelta
from provider.utils import get_dom, on_workdays, days_upper

FB_PAGE = "https://www.facebook.com/inputbistro/posts"
FB_ID = "339892963137631"
URL = "https://www.input.hu"

@on_workdays
def get_menu(today):
    day = today.weekday()
    dom = get_dom(URL)
    menu = dom.xpath(f'/html/body//section[@id="service-section"]//div[*[contains(text(), "{ days_upper[day] }")]]/p/text()')
    menu = '<br>'.join(p.strip() for p in menu)

    return menu

menu = {
    'name': 'Input bar',
    'id': 'ib',
    'url': URL,
    'get': get_menu,
    'ttl': timedelta(minutes=40),
    'cards': ["szep"]
}
