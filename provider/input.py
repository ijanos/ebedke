from datetime import datetime, timedelta
from provider.utils import get_dom, on_workdays, skip_empty_lines

FB_PAGE = "https://www.facebook.com/inputbistro/posts"
FB_ID = "339892963137631"
URL = "https://www.input.hu/#service-section"

@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    menu = dom.xpath(f'/html/body//div[@class="_serviceContainer"]//text()')
    menu = '<br>'.join(skip_empty_lines(line for line in menu if "menü" not in line.lower()))

    return menu

menu = {
    'name': 'Input bar',
    'id': 'ib',
    'url': URL,
    'get': get_menu,
    'ttl': timedelta(minutes=90),
    'cards': ["szep"]
}
