from datetime import datetime, timedelta
from itertools import dropwhile, islice
from provider.utils import get_filtered_fb_post, days_lower, skip_empty_lines


FB_PAGE = "https://www.facebook.com/pg/KompotBisztro/posts/"
FB_ID = "405687736167829"

def getMenu(today):
    menu = ''
    try:
        day = today.weekday()
        is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
        is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
        line_filter = lambda line: "leves" in line or \
                                   "a:" in line or \
                                   "b:" in line
        daily_menu_filter = lambda post: is_today(post['created_time']) \
                                and "menü" in post['message'].lower()
        weekly_menu_filter = lambda post: is_this_week(post['created_time']) \
                                and days_lower[day] in post['message'].lower()
        weekly_menu = get_filtered_fb_post(FB_ID, weekly_menu_filter)
        if weekly_menu:
            menu = dropwhile(lambda line: days_lower[day] not in line.lower(), skip_empty_lines(weekly_menu.split('\n')))
        else:
            menu = get_filtered_fb_post(FB_ID, daily_menu_filter).split('\n')
        menu = filter(lambda line: line_filter(line.lower()), menu)
        menu = islice(menu, 3)
        menu = "<br>".join(menu)
    except:
        pass

    return {
        'name': 'Kompót',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
