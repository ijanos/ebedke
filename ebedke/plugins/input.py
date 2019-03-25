from datetime import datetime, timedelta
from ebedke.utils.utils import get_dom, on_workdays, skip_empty_lines, pattern_slice
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/inputbistro/posts"
FB_ID = "339892963137631"
URL = "https://www.input.hu/?page_id=1981"

@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    page = dom.xpath("/html/body//div[@id='heti-men-page']//text()")
    looks_like_a_date = lambda text: text.count(".") > 2 and str(today.year) in text
    date = next(filter(looks_like_a_date, page))
    date = datetime.strptime(date.split("-")[0].strip(" ."), "%Y.%m.%d")

    if date <= today < date + timedelta(days=6):
        menu = page
    else:
        menu = []

    menu = pattern_slice(menu, ["levesek"], ["étlap", "function", "getElementById"])
    return menu


plugin = EbedkePlugin(
    enabled=True,
    name='Input bar',
    id='ib',
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=["szep"],
    groups=["corvin"]
)
