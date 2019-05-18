from datetime import datetime, timedelta
from ebedke.utils.utils import get_filtered_fb_post, on_workdays, pattern_slice
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/lanubecafe/posts"
FB_ID = "1652899941600571"

@on_workdays
def get_menu(today):
    def fb_filter(post):
        created = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
        trigger_words = ["menü", "fogás"]
        more_than_5_lines = post["message"].count("\n") > 5
        triggered = any(word in post["message"].lower() for word in trigger_words)
        this_week = created.date() <= today.date() < created.date() + timedelta(days=7)
        return this_week and triggered and more_than_5_lines

    menu = get_filtered_fb_post(FB_ID, fb_filter)
    menu = menu.split('\n')
    return pattern_slice(menu, ["fogás"], ["following", "plate"])

plugin = EbedkePlugin(
    enabled=True,
    name='La Nube',
    id='nube',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    groups=["moricz"]
)
