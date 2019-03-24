from datetime import datetime, timedelta
from ebedke.utils.utils import get_dom, on_workdays, skip_empty_lines
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/inputbistro/posts"
FB_ID = "339892963137631"
URL = "https://www.input.hu/?page_id=1981"

@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    date = dom.xpath(f"/html/body//div/h2[contains(text(), {today.year})]/text()")
    date = date.pop() if date else None
    date = datetime.strptime(date.split("-")[0], "%Y.%m.%d")

    if date <= today < date + timedelta(days=6):
        menu = dom.xpath("/html/body//div[p and ul]//text()")
    else:
        menu = []

    drop_words = ["fogásos"]
    menu = filter(lambda line: not any(word in line.lower() for word in drop_words), menu)
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
