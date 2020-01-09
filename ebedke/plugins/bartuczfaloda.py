from datetime import timedelta
from ebedke.utils.date import on_workdays
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/pg/bartuczfaloda/posts"
FB_ID = "104053327664944"

@on_workdays
def get_menu(_today):
    return []

plugin = EbedkePlugin(
    enabled=True,
    name='Bartucz Faloda',
    id='baf',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=23),
    cards=[],
    groups=["corvin"],
    coord=(47.485874, 19.070868)
)
