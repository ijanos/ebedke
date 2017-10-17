from datetime import datetime, timedelta
from provider.utils import get_facebook_posts


URL = "https://www.facebook.com/PortumCorvin/posts/"
FB_ID = "728866253985071"

def getMenu(today):
    posts = get_facebook_posts(FB_ID)
    parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
    menu = next((p for p in posts
                 if parse_date(p['created_time']) > today.date() - timedelta(days=7)
                 and "menü" in p['message'].lower()),
                {'message': ''})

    menu = menu['message']
    if "Előételek:" in menu:
        menu = menu.split("Előételek:")[1].strip()
    menu = '<br>'.join(i for i in menu.split('\n') if i)

    return {
        'name': 'Portum',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
