from datetime import timedelta
from ebedke.utils.utils import get_dom, skip_empty_lines, days_lower, on_workdays, pattern_slice
from ebedke.pluginmanager import EbedkePlugin


URL_ROOT = "http://stexhaz.hu/index.php/hu/etl/deli-ajanlat"


@on_workdays
def get_menu(today):
    dom = get_dom(URL_ROOT)
    menu = dom.xpath("/html/body//article//text()")
    menu = pattern_slice(menu, [days_lower[today.weekday()]], days_lower + ['ára', 'előfizetés', 'ajánlat'], inclusive=False)
    return list(skip_empty_lines(menu))


plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Stex',
    id="st",
    url=URL_ROOT,
    downloader=get_menu,
    ttl=timedelta(minutes=25),
    cards=['szep', 'erzs']
)
