from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, skip_empty_lines, on_workdays


FB_PAGE = "https://www.facebook.com/Nine-Tables-Corvin-255153518398246/"
FB_ID = "255153518398246"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_words = ["mai menü", "napi menü"]
    menu_filter = lambda post: is_today(post['created_time']) and any(word in post['message'].lower() for word in menu_words)
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    if menu:
        drop_words = ["#", "napi menü", '"', "hétvég", "590", "...", "!", "“"]
        menu = filter(lambda l: not any(word in l.lower() for word in drop_words), menu.splitlines())
        menu = ''.join(char for char in '\n'.join(menu) if ord(char) < 500).splitlines()
        return list(skip_empty_lines(menu))
    else:
        return []

menu = {
    'name': 'Nine Tables',
    'id': 'nt',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=24),
    'cards': []
}
