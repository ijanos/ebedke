from datetime import timedelta
from ebedke.pluginmanager import EbedkePlugin

URL = "http://www.jedermann.hu/#napi"
FB_URL = "https://www.facebook.com/pg/jedermann.budapest/posts/"

def get_menu(_today):
    return []

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name="Jedermann",
    id="jdr",
    url=FB_URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.481862, 19.067095)
)
