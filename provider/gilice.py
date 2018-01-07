from datetime import timedelta, datetime
from itertools   import takewhile, dropwhile, islice

from provider.utils import get_filtered_fb_post, days_lower, get_fb_cover_url, skip_empty_lines

FB_PAGE = "https://www.facebook.com/pg/gilicekonyha/posts/"
FB_ID = "910845662306901"

def getFBMenu(today):
    day = today.weekday()
    menu = ''
    try:
        if day < 5:
            is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
            menu_filter = lambda post: is_this_week(post['created_time']) and "jelmagyarázat" in post['message'].lower()
            menu = get_filtered_fb_post(FB_ID, menu_filter)
            post_parts = menu.split("HETI MENÜ")
            if len(post_parts) > 1:
                weekly_menu = post_parts[1]
                menu = weekly_menu.strip().split("\n")
                menu = islice(dropwhile(lambda l: days_lower[day] not in l, menu), 1, None)
                menu = takewhile(lambda l: not any(day in l for day in days_lower), menu)
                menu = '<br>'.join(skip_empty_lines(menu))
            else:
                menu = f'<a href="{get_fb_cover_url(FB_ID)}">heti menü</a>'
    except:
        pass

    if "zárva" in menu.lower():
        menu = ''

    return menu

def getMenu(today):
    if today.weekday() < 5:
        menu = getFBMenu(today)
    else:
        menu = ""

    return menu

menu = {
    'name': 'Gólya',
    'url': FB_PAGE,
    'get': getMenu,
    'ttl': timedelta(hours=3)
}

if __name__ == "__main__":
    print(getMenu(datetime.today()))
