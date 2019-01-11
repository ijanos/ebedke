from datetime import datetime, timedelta
from itertools import dropwhile, islice
from provider.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays, pattern_slice


FB_PAGE = "https://www.facebook.com/pg/kubalabarca/posts/"
FB_ID = "2454065824618853"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()

    menu_filter = lambda post: (is_this_week(post['created_time'])
                               and days_lower[today.weekday()] in post['message'].lower()
                               and "asztalfoglalás" not in post['message'].lower()) \
                               or ("menü" in post['message'].lower()
                                    and is_today(post['created_time'])
                                    and "asztalfoglalás" not in post['message'].lower())

    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = ''.join(char for char in menu if ord(char) < 500)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()], "mai", "menü"], days_lower + ["ár:"])

    return '<br>'.join(skip_empty_lines(menu))

menu = {
    'name': 'Kubala Barcelona',
    'id': 'kbarc',
    'url': FB_PAGE,
    'get': getMenu,
    'ttl': timedelta(hours=24),
    'cards': []
}
