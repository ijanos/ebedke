from datetime import timedelta, datetime
from itertools   import takewhile, dropwhile, islice

from provider.utils import get_filtered_fb_post, days_lower, get_fb_cover_url, skip_empty_lines, on_workdays, pattern_slice

FB_PAGE = "https://www.facebook.com/pg/gilicekonyha/posts/"
FB_ID = "910845662306901"

@on_workdays
def get_menu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() >= today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and "jelmagyarázat" in post['message'].lower()
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()]], days_lower, inclusive=False)
    menu = '<br>'.join(skip_empty_lines(menu))

    return menu

menu = {
    'name': 'Gólya',
    'id': 'gl',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=18),
    'cards': ['szep']
}
