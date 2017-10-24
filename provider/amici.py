from datetime import datetime, timedelta
from provider.utils import get_facebook_posts, days_lower
import re

FB_PAGE = "https://www.facebook.com/pg/amicimieicorvin/posts"
FB_ID = "1861078894105248"


def getMenu(today):
    day = today.weekday()
    try:
        posts = get_facebook_posts(FB_ID)
        parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
        weekly_menu = next((p for p in posts
                            if sum(day in p['message'].lower() for day in days_lower) > 3
                            and parse_date(p['created_time']) > today.date() -  timedelta(days=7)), None)
        menu = weekly_menu['message']
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
