from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, days_lower
import re

FB_PAGE = "https://www.facebook.com/pg/amicimieicorvin/posts"
FB_ID = "1861078894105248"


def getMenu(today):
    day = today.weekday()
    try:
        is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
        menu_filter = lambda post: is_this_week(post['created_time']) and sum(day in post['message'].lower() for day in days_lower) > 3
        menu = get_filtered_fb_post(FB_ID, menu_filter)
        menu = re.split('(hétfő|kedd|szerda|csütörtök|péntek):', menu, flags=re.IGNORECASE)
        menu = dict(zip([str.lower(d) for d in menu[1::2]], menu[2::2]))
        menu = menu[days_lower[day]]
        menu = '<br>'.join(menu.strip().split('\n'))
    except:
        menu = ''

    return {
        'name': 'Amici Miei',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
