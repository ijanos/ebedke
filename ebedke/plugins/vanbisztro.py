from datetime import datetime, timedelta
from utils.utils import get_filtered_fb_post, days_lower, skip_empty_lines, on_workdays, pattern_slice
from plugin import EbedkePlugin


FB_PAGE = "https://www.facebook.com/pg/vanbisztro/posts/"
FB_ID = "168579617153632"


def fb_filter(post, today):
    created = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
    not_too_long = len(post["message"]) < 160
    today_morning = created.date() == today.date() and 9 <= created.hour < 13
    return not_too_long and today_morning


@on_workdays
def getMenu(today):
    fbfilter = lambda post: fb_filter(post, today)
    menu = get_filtered_fb_post(FB_ID, fbfilter)
    drop_words = ["menü"] + days_lower
    menu = filter(lambda line: not any(word in line.lower() for word in drop_words), menu.splitlines())
    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["szell"],
    name='VAN bisztró',
    id='van',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[]
)
