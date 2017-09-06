from datetime import datetime
from provider.utils import get_facebook_posts

FB_PAGE = "https://www.facebook.com/pg/KompotBisztro/posts/"
FB_ID = "405687736167829"

def getMenu(today):
    posts = get_facebook_posts(FB_ID)
    parse_date = lambda d: datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z').date()
    menu = next((p for p in posts['data']
                 if parse_date(p['created_time']) == today.date()
                 and ("menü" in p['message'] or "étvágyat" in p['message'])),
                {'message': ''})

    menu = ' '.join(filter(lambda s: s[0] is not '#', menu['message'].split())) # remove hashtags
    menu = ''.join(char for char in menu if ord(char) < 1000) # remove emojis
    menu = menu.replace("A:", "<br>A:")
    menu = menu.replace("B:", "<br>B:")

    return {
        'name': 'Kompót',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
