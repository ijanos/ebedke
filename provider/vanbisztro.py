from datetime import datetime, timedelta
from itertools import dropwhile, islice
from provider.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays, pattern_slice


FB_PAGE = "https://www.facebook.com/pg/vanbisztro/posts/"
FB_ID = "168579617153632"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()

    menu_filter = lambda post: (is_this_week(post['created_time']) \
                               and days_lower[today.weekday()] in post['message'].lower()) \
                               or ("menü" in post['message'].lower() and is_today(post['created_time']))

    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()], "mai", "menü"], days_lower + ["ár:"])

    menu = '<br>'.join(skip_empty_lines(menu))
    menu = ''.join([c if ord(c) < 500 else '' for c in menu])

    return menu

menu = {
    'name': 'VAN bisztró',
    'id': 'van',
    'url': FB_PAGE,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': []
}
