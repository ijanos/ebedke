from datetime import datetime, timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/vegasarok/posts"
FB_ID = "148178981897532"

def fb_filter(post, today):
    created = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
    trigger_words = ["menü"]
    more_than_5_lines = post["message"].count("\n") > 5
    triggered = any(word in post["message"].lower() for word in trigger_words)
    return created.date() == today.date() and triggered and more_than_5_lines

@on_workdays
def get_menu(today):
    fbfilter = lambda post: fb_filter(post, today)
    menu = facebook.get_filtered_post(FB_ID, fbfilter)
    drop_words = ["menü!", "jó étvágyat"]
    menu = filter(lambda line: not any(word in line.lower() for word in drop_words), menu.splitlines())
    return menu

plugin = EbedkePlugin(
    enabled=True,
    name='Govinda',
    id='gov',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["ferenciek"],
    coord=(47.490800, 19.056685)
)
