from datetime import datetime, timedelta
from itertools import dropwhile, islice
from provider.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays


FB_PAGE = "https://www.facebook.com/pg/amicimieicorcin/posts"
FB_ID = "1861078894105248"

@on_workdays
def getMenu(today):
    day = today.weekday()
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and sum(day in post['message'].lower() for day in days_lower) >= 2
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = dropwhile(lambda line: days_lower[day] not in line.lower(), skip_empty_lines(menu.splitlines()))
    menu = islice(menu, 1, 4)
    menu = '<br>'.join(menu).replace("�", "")

    return menu


menu = {
    'name': 'Amici Miei',
    'url': FB_PAGE,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['bank', 'szep']
}
