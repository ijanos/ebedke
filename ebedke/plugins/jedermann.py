from datetime import timedelta, date
from re import split
from utils.utils import get_dom, on_workdays, days_lower, pattern_slice
from utils.date import parse_hungarian_month
from plugin import EbedkePlugin


URL = "http://www.jedermann.hu/#napi"


@on_workdays
def get_menu(today):
    dom = get_dom(URL, force_utf8=True)
    menudate = ''.join(dom.xpath('/html/body//div[@id="datum"]//text()'))
    start_month, start_day, *_ = split(" |-", menudate)
    menu_start_date = date(today.year, parse_hungarian_month(start_month), int(start_day))
    if menu_start_date <= today.date() < menu_start_date + timedelta(days=7):
        menu = dom.xpath('/html/body//div[preceding-sibling::div[@id="datum"]]//article[@class="lmenu"]//text()')
        menu = pattern_slice(menu, [days_lower[today.weekday()]], days_lower)
    else:
        menu = []
    return menu


plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name="Jedermann",
    id="jdr",
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[]
)
