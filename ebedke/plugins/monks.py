from datetime import datetime, timedelta
import re
from ebedke.utils.utils import on_workdays, days_lower
from ebedke.utils.http import get_dom
from ebedke.pluginmanager import EbedkePlugin


URL = "http://www.monks.hu/etlap"

@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    week_date = dom.xpath("/html/body//div//li//a[contains(text(), 'MENÜ')]/text()")
    from_date, to_date = re.split(r" |-", week_date.pop())[-2:]
    from_date = datetime.strptime(f"{today.year}.{from_date}", "%Y.%m.%d.")
    to_date = datetime.strptime(f"{today.year}.{to_date}", "%Y.%m.%d.")

    menu = []
    if from_date.date() <= today.date() <= to_date.date():
        rows = dom.xpath("/html/body//tr[count(td)=2]")
        for row in rows:
            if days_lower[today.weekday()] in row.text_content().lower():
                menu = row.xpath(".//td[2]//text()")
    return menu


plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name="Monks",
    id="mo",
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[],
    coord=(47.492625, 19.052698)
)
