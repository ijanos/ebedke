from datetime import datetime, timedelta
from io import BytesIO
from itertools import dropwhile, takewhile
from PIL import Image
from provider.utils import get_fb_post_attached_image, get_filtered_fb_post, on_workdays, ocr_image, days_lower_ascii, pattern_slice, remove_accents


FB_PAGE = "https://www.facebook.com/pg/kerovaetelbar/posts/"
FB_ID = "582373908553561"

def read_image(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and "heti" in post['message'].lower()
    image = get_fb_post_attached_image(FB_ID, menu_filter)
    if image:
        _, image, _ = Image.open(BytesIO(image)).split()
        f = BytesIO()
        image.save(f, format="png", optimize=True)
        menu = ocr_image(f).splitlines()
        if not menu:
            return ""

        day = today.weekday()
        menu = dropwhile(lambda l: days_lower[day] not in l.lower(), menu)
        head = next(menu)
        stopwords = days_lower + ["falatozz", "práter"]
        menu = takewhile(lambda l: not any(word in l.lower() for word in stopwords), menu)
        menu = f'{head} {" ".join(menu)}'
        menu = menu.split(":")[1].strip() if ":" in menu else menu
        return menu
    else:
        return ""

@on_workdays
def get_menu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    contains_days = lambda post: sum(day in post for day in days_lower_ascii) > 2
    menu_filter = lambda post: is_this_week(post['created_time']) and contains_days(remove_accents(post['message'].lower()))
    menu = get_filtered_fb_post(FB_ID, menu_filter)
    m = lambda p: remove_accents(p.lower())
    menu = pattern_slice(menu.splitlines(), [days_lower_ascii[today.weekday()]], days_lower_ascii, inclusive=True, modifier=m)
    menu = ' '.join(menu)
    if ':' in menu:
        menu = menu.split(':')[1].strip()
    return menu

menu = {
    'name': 'Kerova',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=23),
    'cards': []
}
