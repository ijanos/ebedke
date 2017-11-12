import re
from datetime import datetime, timedelta
from provider.utils import get_filtered_fb_post, days_lower


FB_PAGE = "https://www.facebook.com/pg/KompotBisztro/posts/"
FB_ID = "405687736167829"


def cleanup(text):
    text = ' '.join(filter(lambda s: s[0] is not '#', text.split())) # remove hashtags
    text = ''.join(char for char in text if ord(char) < 1000) # remove emojis
    return text

def clean_up_weekly_menu(menu, day):
    menu = re.split('(hétfő|kedd|szerda|csütörtök|péntek):', menu, flags=re.IGNORECASE)
    menu = dict(zip([str.lower(d) for d in menu[1::2]], menu[2::2]))
    menu = cleanup(menu[days_lower[day]])
    menu = menu.replace("A:", "<br>A:")
    menu = menu.replace("B:", "<br>B:")
    menu = '<br>'.join(menu.strip().split('\n'))
    return menu

def clean_up_daily_menu(menu):
    menu = cleanup(menu)
    menu = menu.replace("A:", "<br>A:")
    menu = menu.replace("B:", "<br>B:")
    return menu

def getMenu(today):
    menu = ''
    try:
        is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
        is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
        daily_menu_filter = lambda post: is_today(post['created_time']) \
                                and "étvágyat" in post['message'].lower() \
                                and "heti" not in post['message'].lower()
        weekly_menu_filter = lambda post: is_this_week(post['created_time']) \
                                and "heti menü" in post['message'].lower()
        daily_menu = get_filtered_fb_post(FB_ID, daily_menu_filter)
        weekly_menu = get_filtered_fb_post(FB_ID, weekly_menu_filter)
        if daily_menu:
            menu = clean_up_daily_menu(daily_menu)
        elif weekly_menu:
            menu = clean_up_weekly_menu(weekly_menu['message'], today.weekday())
    except:
        pass

    return {
        'name': 'Kompót',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
