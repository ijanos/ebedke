from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, skip_empty_lines, on_workdays


FB_PAGE = "https://www.facebook.com/Nine-Tables-Corvin-255153518398246/"
FB_ID = "255153518398246"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_filter = lambda post: is_today(post['created_time']) and "napi menü" in post['message'].lower()
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    menu = ''.join(char for char in menu if ord(char) < 500)
    drop_words = ["#", "napi menü", '"', "hétvég", "590", "...", "!", "“"]
    menu = skip_empty_lines(filter(lambda l: not any(word in l.lower() for word in drop_words), menu.splitlines()))
    return list(menu)

menu = {
    'name': 'Nine Tables',
    'id': 'nt',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=24),
    'cards': []
}
