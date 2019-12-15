from typing import List
from datetime import timedelta, datetime
from ebedke.utils.utils import on_workdays
from ebedke.utils import http
from ebedke.pluginmanager import EbedkePlugin


URL = "https://www.kajahu.com/etlap/d"
API = "https://appif.kajahu.com/jdmenu?jlang=hu&jseat=-"


@on_workdays
def getMenu(today: datetime) -> List[str]:
    date = today.strftime("%Y-%m-%d")
    menujson = http.get(API).json()
    menu: List[str] = []
    for day in menujson['jdata']:
        if day['ddate'] == date:
            menukeys = ["line1", "line2", "line3", "soup", "main", "drink", "dessert"]
            menu += [day[key] for key in day.keys() if key in menukeys and day[key] is not None]

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek", "corvin"],
    name='KAJAHU',
    id='kjh',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    coord=[(47.494301, 19.054397), (47.485758, 19.076788)]
)
