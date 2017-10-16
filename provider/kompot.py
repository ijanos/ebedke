from datetime import datetime, timedelta
from provider.utils import get_facebook_posts

FB_PAGE = "https://www.facebook.com/pg/KompotBisztro/posts/"
FB_ID = "405687736167829"

def clean_up_weekly_menu(menu, day):
    day_names = ["Hétfő:", "Kedd:", "Szerda:", "Csütörtök:", "Péntek:"]
    menu = menu.strip().split("\n\n")[day + 1]
    menu = menu.replace(day_names[day], '')
    menu = '<br>'.join(menu.strip().split('\n'))
    return menu

def clean_up_daily_menu(menu):
    menu = ' '.join(filter(lambda s: s[0] is not '#', menu.split())) # remove hashtags
    menu = ''.join(char for char in menu if ord(char) < 1000) # remove emojis
    menu = menu.replace("A:", "<br>A:")
    menu = menu.replace("B:", "<br>B:")
    return menu

def getMenu(today):
    posts = get_facebook_posts(FB_ID)
    parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
    weekly_menu = next((p for p in posts['data']
                        if "heti menü" in p['message'].lower()
                        and parse_date(p['created_time']) > today.date() - timedelta(days=6)), None)
    daily_menu = next((p for p in posts['data']
                       if parse_date(p['created_time']) == today.date()
                       and "étvágyat" in p['message'].lower()
                       and "heti" not in p['message'].lower()), None)

    if daily_menu:
        menu = clean_up_daily_menu(daily_menu['message'])
    elif weekly_menu:
        menu = clean_up_weekly_menu(weekly_menu['message'], today.weekday())
    else:
        menu = ''

    return {
        'name': 'Kompót',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
