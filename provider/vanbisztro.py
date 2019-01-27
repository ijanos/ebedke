from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays, pattern_slice


FB_PAGE = "https://www.facebook.com/pg/vanbisztro/posts/"
FB_ID = "168579617153632"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()

    menu_filter = lambda post: (is_this_week(post['created_time'])
                               and days_lower[today.weekday()] in post['message'].lower()) \
                               or ("menü" in post['message'].lower() and is_today(post['created_time']))

    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()], "mai", "menü"], days_lower + ["ár:"])

    remove_emoji = lambda text: ''.join(char for char in text if ord(char) < 500)
    menu = [remove_emoji(m) for m in skip_empty_lines(menu)]

    return menu

menu = {
    'name': 'VAN bisztró',
    'id': 'van',
    'url': FB_PAGE,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': []
}
