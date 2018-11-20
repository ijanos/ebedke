from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, on_workdays, skip_empty_lines


FB_PAGE = "https://www.facebook.com/aranytacsko/posts"
FB_ID = "211285456287124"

@on_workdays
def get_menu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_filter = lambda post: is_today(post['created_time']) and \
        any(word in post['message'].lower() for word in ["ebédmenü", "ebéd menü", "mai menü", "déli menü", "mai ebéd", "ajánlat"])
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    drop_words = ["ajánlat", "tacskó", "ebéd", "menü"]
    menu = '<br>'.join(skip_empty_lines(filter(lambda l: not any(word in l.lower() for word in drop_words), menu.splitlines())))
    return menu

menu = {
    'name': 'Arany Tacskó bistro',
    'id': 'tc',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=23),
    'cards': []
}
