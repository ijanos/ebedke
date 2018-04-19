from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, on_workdays


URL = "https://www.facebook.com/PortumCorvin/posts/"
FB_ID = "728866253985071"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    many_colons = lambda msg: msg.count(':') > 4
    menu_filter = lambda post: is_this_week(post['created_time']) and many_colons(post['message'])
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = [line for line in menu.splitlines() if line.strip().startswith('-')]
    menu = '<br>'.join(menu)

    return menu

menu ={
    'name': 'Portum',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': []
}
