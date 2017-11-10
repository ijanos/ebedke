from datetime import datetime
from itertools import dropwhile
from provider.utils import get_filtered_fb_post


FB_PAGE = "https://www.facebook.com/pg/Foodie-MinuteBistro-494549960697458/posts"
FB_ID = "494549960697458"


def getMenu(today):
    try:
        is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
        menu_filter = lambda post: is_today(post['created_time']) and "leveseink" in post['message'].lower()
        dailymenu = get_filtered_fb_post(FB_ID, menu_filter)
        starts_with_dash = lambda line: len(line) > 1 and (line[0] == '-')
        menu = [line for line in dailymenu.split('\n') if starts_with_dash(line.strip())]
        menu = '<br>'.join(menu)
    except:
        menu = ''

    return {
        'name': 'Foodie',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
