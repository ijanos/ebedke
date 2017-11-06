import re
from datetime import datetime, timedelta
from provider.utils import get_facebook_posts, days_lower
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
    try:
        posts = get_facebook_posts(FB_ID)
        parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
        weekly_menu = next((p for p in posts
                            if "heti menü" in p['message'].lower()
                            and parse_date(p['created_time']) > today.date() - timedelta(days=6)), None)
        daily_menu = next((p for p in posts
                           if parse_date(p['created_time']) == today.date()
                           and "étvágyat" in p['message'].lower()
                           and "heti" not in p['message'].lower()), None)
        if daily_menu:
            menu = clean_up_daily_menu(daily_menu['message'])
        elif weekly_menu:
            menu = clean_up_weekly_menu(weekly_menu['message'], today.weekday())
    except:
        menu = ''

    return {
        'name': 'Kompót',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
