from datetime import datetime as dt, timedelta
from provider.utils import get_filtered_fb_post, on_workdays


FB_PAGE = "https://www.facebook.com/pg/Foodie-MinuteBistro-494549960697458/posts"
FB_ID = "494549960697458"

@on_workdays
def getMenu(today):
    is_today = lambda date: dt.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_filter = lambda post: is_today(post['created_time']) and "leveseink" in post['message'].lower()
    dailymenu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = [line for line in dailymenu.splitlines() if line.strip().startswith('-')]
    menu = '<br>'.join(menu)
    return menu

menu = {
    'name': 'Foodie',
    'id': 'fd',
    'url': FB_PAGE,
    'get': getMenu,
    'ttl': timedelta(hours=8),
    'cards': ['szep', 'erzs']
}
