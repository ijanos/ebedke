from datetime import datetime, timedelta
from provider.utils import get_dom, on_workdays, skip_empty_lines

FB_PAGE = "https://www.facebook.com/inputbistro/posts"
FB_ID = "339892963137631"
URL = "https://www.input.hu/?page_id=1981"

@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    date = dom.xpath(f"/html/body//div/h2[contains(text(), {today.year})]/text()")
    date = date.pop() if date else None
    date = datetime.strptime(date.split("-")[0], "%Y.%m.%d")

    if today - timedelta(days=7) < date:
        menu = dom.xpath("/html/body//div[p and ul]//text()")
    else:
        menu = []
    return list(skip_empty_lines(menu))

menu = {
    'name': 'Input bar',
    'id': 'ib',
    'url': URL,
    'get': get_menu,
    'ttl': timedelta(minutes=90),
    'cards': ["szep"]
}
