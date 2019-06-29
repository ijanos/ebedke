from datetime import datetime, timedelta
from ebedke.utils.utils import on_workdays, skip_empty_lines
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin

URL = "https://www.facebook.com/PortumCorvin/posts/"
FB_ID = "728866253985071"

@on_workdays
def getMenu(today):
    is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
    triggers = ["lunch menü ", "business lunch", "előételek", "déli menü", "heti menü", "menünk"]
    menu_filter = lambda post: is_this_week(post['created_time']) and \
        any(word in post['message'].lower() for word in triggers) and \
        post['message'].count("\n") > 5
    menu = facebook.get_filtered_post(FB_ID, menu_filter)
    drop_words = ["előételek", "főételek", "desszer", "étvágy", "menü", "lunch", str(today.year), "várunk"]
    menu = skip_empty_lines(filter(lambda l: not any(word in l.lower() for word in drop_words), menu.splitlines()))


    return list(menu)

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Portum',
    id='pt',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    coord=(47.485987, 19.076051)
)
