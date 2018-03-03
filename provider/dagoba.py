from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, on_workdays, skip_empty_lines


FB_PAGE = "https://www.facebook.com/pg/Dagoba-bisztró-1742309292469507/posts"
FB_ID = "1742309292469507"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    many_colons = lambda msg: msg.count(':') > 4
    menu_filter = lambda post: is_today(post['created_time']) and many_colons(post['message'])
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    drop = lambda l: not l.strip().endswith((':', '!', '.', ','))
    menu = '<br>'.join(skip_empty_lines((filter(drop, menu.splitlines()))))
    return menu

menu = {
    'name': 'Dagoba',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=23),
    'cards': ['bank']
}
