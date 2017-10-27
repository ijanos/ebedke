from datetime import datetime
from provider.utils import get_filtered_fb_post


FB_PAGE = "https://www.facebook.com/pg/Foodie-MinuteBistro-494549960697458/posts"
FB_ID = "494549960697458"


def getMenu(today):
    try:
        is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
        menu_filter = lambda post: is_today(post['created_time']) and "leveseink" in post['message'].lower()
        dailymenu = get_filtered_fb_post(FB_ID, menu_filter)
        dailymenu = dailymenu.split("Leveseink:")[1]
        menu = []
        for line in dailymenu.split('\n'):
            line = line.strip()
            if len(line) > 1 and (line[0] == '-' or line[-1] == ':'):
                menu.append(line)
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
