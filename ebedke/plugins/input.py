from datetime import timedelta
from ebedke.utils.date import on_workdays
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/inputkitchenandbar"
URL = "https://www.input.hu/?page_id=1981"

@on_workdays
def get_menu(_):
    return []


plugin = EbedkePlugin(
    enabled=True,
    name='Input bar',
    id='ib',
    url=FB_PAGE,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=["szep"],
    groups=["corvin"],
    coord=(47.485573, 19.064700)
)
