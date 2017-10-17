from datetime import datetime, timedelta
from provider.utils import get_facebook_posts
import re

FB_PAGE = "https://www.facebook.com/pg/amicimieicorvin/posts"
FB_ID = "1861078894105248"


def getMenu(today):
    day_names = ["hétfő", "kedd", "szerda", "csütörtök", "péntek"]
    try:
        posts = get_facebook_posts(FB_ID)
        parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
        weekly_menu = next((p for p in posts['data']
                            if all(day in p['message'].lower() for day in day_names)
                            and parse_date(p['created_time']) > today.date() -  timedelta(days=7)), None)
        menu = weekly_menu['message']
        menu = re.split("Hétfő:|Kedd:|Szerda:|Csütörtök:|Péntek:", menu)[today.weekday() + 1]
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
