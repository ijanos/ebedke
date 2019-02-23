from datetime import timedelta
from provider.utils import get_dom, skip_empty_lines, days_lower, on_workdays, pattern_slice

URL_ROOT = "http://stexhaz.hu/index.php/hu/etl/deli-ajanlat"


@on_workdays
def get_menu(today):
    dom = get_dom(URL_ROOT)
    menu = dom.xpath("/html/body//article//text()")
    menu = pattern_slice(menu, [days_lower[today.weekday()]], days_lower + ['ára', 'előfizetés', 'ajánlat'], inclusive=False)
    return list(skip_empty_lines(menu))

menu = {
    'name': 'Stex',
    'id': "st",
    'url': URL_ROOT,
    'get': get_menu,
    'ttl': timedelta(minutes=25),
    'cards': ['szep', 'erzs']
}
