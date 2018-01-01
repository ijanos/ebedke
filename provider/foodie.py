from datetime import datetime as dt, timedelta
from provider.utils import get_filtered_fb_post


FB_PAGE = "https://www.facebook.com/pg/Foodie-MinuteBistro-494549960697458/posts"
FB_ID = "494549960697458"


def getMenu(today):
    try:
        is_today = lambda date: dt.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
        menu_filter = lambda post: is_today(post['created_time']) and "leveseink" in post['message'].lower()
        dailymenu = get_filtered_fb_post(FB_ID, menu_filter)
        menu = [line for line in dailymenu.split('\n') if line.strip().startswith('-')]
        menu = '<br>'.join(menu)
    except:
        menu = ''

    return menu

menu = {
    'name': 'Foodie',
    'url': FB_PAGE,
    'get': getMenu,
    'ttl': timedelta(hours=4)
}

if __name__ == "__main__":
    print(getMenu(dt.today()))
