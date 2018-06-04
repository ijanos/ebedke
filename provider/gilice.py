from datetime import timedelta, datetime
from itertools   import takewhile, dropwhile, islice

from provider.utils import get_filtered_fb_post, days_lower, get_fb_cover_url, skip_empty_lines, on_workdays

FB_PAGE = "https://www.facebook.com/pg/gilicekonyha/posts/"
FB_ID = "910845662306901"

@on_workdays
def get_menu(today):
    day = today.weekday()
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() >= today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and "jelmagyarázat" in post['message'].lower()
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    post_parts = menu.split("HETI MENÜ")
    if len(post_parts) > 1:
        weekly_menu = post_parts[1]
        menu = weekly_menu.strip().split("\n")
        menu = islice(dropwhile(lambda l: days_lower[day] not in l, menu), 1, None)
        menu = takewhile(lambda l: not any(day in l for day in days_lower), menu)
        menu = '<br>'.join(skip_empty_lines(menu))
    elif menu:
        menu = f'<a href="{get_fb_cover_url(FB_ID)}">heti menü</a>'
    else:
        menu = ''

    return menu

menu = {
    'name': 'Gólya',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=18),
    'cards': ['szep']
}
