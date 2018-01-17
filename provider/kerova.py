from datetime import datetime, timedelta
from io import BytesIO
from itertools import dropwhile, takewhile
from PIL import Image
from provider.utils import get_fb_post_attached_image, on_workdays, ocr_image, days_lower


FB_PAGE = "https://www.facebook.com/kerovaetelbar/"
FB_ID = "582373908553561"

@on_workdays
def get_menu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    menu_filter = lambda post: is_this_week(post['created_time']) and "heti" in post['message'].lower()
    image = get_fb_post_attached_image(FB_ID, menu_filter)
    if image:
        _, image, _ = Image.open(BytesIO(image)).split()
        f = BytesIO()
        image.save(f, format="png", optimize=True)
        menu = ocr_image(f).splitlines()

        day = today.weekday()
        menu = dropwhile(lambda l: days_lower[day] not in l.lower(), menu)
        head = next(menu)
        menu = takewhile(lambda l: not any(day in l.lower() for day in days_lower), menu)
        menu = f'{head} {" ".join(menu)}'.split(":")[1].strip()
        return menu
    else:
        return ""


menu = {
    'name': 'Kerova',
    'url': FB_PAGE,
    'get': get_menu,
    'ttl': timedelta(hours=23)
}

if __name__ == "__main__":
    print(get_menu(datetime.today()))
