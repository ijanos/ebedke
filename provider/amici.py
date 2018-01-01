from datetime import datetime, timedelta
from itertools import dropwhile, islice
from provider.utils import get_filtered_fb_post, days_lower, skip_empty_lines


FB_PAGE = "https://www.facebook.com/pg/amicimieicorcin/posts"
FB_ID = "1861078894105248"



def getMenu(today):
    day = today.weekday()
    try:
        is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
        menu_filter = lambda post: is_this_week(post['created_time']) and sum(day in post['message'].lower() for day in days_lower) > 3
        menu = get_filtered_fb_post(FB_ID, menu_filter)
        menu = dropwhile(lambda line: days_lower[day] not in line.lower(), skip_empty_lines(menu.split('\n')))
        menu = islice(menu, 1, 4)
        menu = '<br>'.join(menu)
    except:
        menu = ''

    return menu


menu = {
    'name': 'Amici Miei',
    'url': FB_PAGE,
    'get': getMenu,
    'ttl': timedelta(hours=5)
}

if __name__ == "__main__":
    print(getMenu(datetime.today()))
