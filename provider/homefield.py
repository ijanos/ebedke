from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays, pattern_slice


FB_PAGE = "https://www.facebook.com/HomeFieldPub/"
FB_ID = "190139087785846"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=6)
    menu_filter = lambda post: is_this_week(post['created_time']) and sum(day in post['message'].lower() for day in days_lower) >= 2
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = ''.join(char for char in menu if ord(char) < 500)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower + ["tel:", "797"])

    return '<br>'.join(skip_empty_lines(menu))

menu = {
    'name': 'HomeField Pub',
    'id': 'hfp',
    'url': FB_PAGE,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': []
}
