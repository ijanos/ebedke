from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, on_workdays, skip_empty_lines

FB_PAGE = "https://www.facebook.com/szatyorbar/posts"
FB_ID = "140232679345332"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_filter = lambda post: is_today(post['created_time']) and "menü" in post['message'].lower()
    menu = get_filtered_fb_post(FB_ID, menu_filter).splitlines()
    menu = list(skip_empty_lines(line.strip() for line in menu if "menü" not in line.lower()))

    return menu

menu = {
    'name': 'Szatyor',
    'id': 'sz',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=23),
    'cards': []
}
