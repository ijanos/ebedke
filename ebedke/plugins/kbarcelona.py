from datetime import datetime, timedelta
from ebedke.utils.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays, pattern_slice
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/kubalabarca/posts/"
FB_ID = "2454065824618853"

def fb_filter(post, today):
    more_than_5_lines = post["message"].count("\n") > 5
    created = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
    trigger_words = ["menünk", "leves", "menü", days_lower[today.weekday()]]
    triggered = any(word in post["message"].lower() for word in trigger_words)
    is_today = today.date() == created.date()
    return triggered and is_today and more_than_5_lines


@on_workdays
def getMenu(today):
    fbfilter = lambda post: fb_filter(post, today)
    menu = get_filtered_fb_post(FB_ID, fbfilter)
    menu = pattern_slice(menu.splitlines(), [days_lower[today.weekday()], "mai", "menü"], days_lower + ["ár:"])

    return list(skip_empty_lines(menu))


plugin = EbedkePlugin(
    enabled=True,
    groups=["szell"],
    name='Kubala Barcelona',
    id='kbarc',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[]
)
