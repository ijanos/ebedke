from datetime import datetime, timedelta
from itertools import dropwhile
from provider.utils import get_filtered_fb_post, days_lower, skip_empty_lines


FB_PAGE = "https://www.facebook.com/pg/KompotBisztro/posts/"
FB_ID = "405687736167829"

def getMenu(today):
    menu = ''
    try:
        day = today.weekday()
        is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
        is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
        ignore_hashtags = lambda post: " ".join(word.lower() for word in post.split() if word[0] != "#")
        daily_menu_filter = lambda post: is_today(post['created_time']) \
                                and "menü" in post['message'].lower()
        weekly_menu_filter = lambda post: is_this_week(post['created_time']) \
                                and days_lower[day] in ignore_hashtags(post['message'])
        weekly_menu = get_filtered_fb_post(FB_ID, weekly_menu_filter)
        if weekly_menu:
            menu_post = dropwhile(lambda line: days_lower[day] not in line.lower(), skip_empty_lines(weekly_menu.split('\n')))
        else:
            menu_post = get_filtered_fb_post(FB_ID, daily_menu_filter).split('\n')
        menu_post = list(menu_post)

        for i, line in enumerate(menu_post):
            if "A:" in line:
                menu = "<br>".join((menu_post[i-1], menu_post[i], menu_post[i+1]))
                break
        if menu == '':
            skipfilter = lambda l:  not any(i in l.lower() for i in ["sütiket", "#", "jó étvágyat", "mai menü"])
            menu = "<br>".join(filter(skipfilter, menu_post))

    except:
        pass

    return {
        'name': 'Kompót',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
