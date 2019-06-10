from typing import List
from datetime import timedelta
from ebedke.utils.utils import on_workdays
from ebedke.utils import http
from ebedke.pluginmanager import EbedkePlugin


URL = "https://www.kajahu.com/etlap/d"
API = "https://appif.kajahu.com/jdmenu?jlang=hu&jseat=-"


@on_workdays
def getMenu(today) -> List[str]:
    date = today.strftime("%Y-%m-%d")
    menujson = http.get(API).json()
    menu: List[str] = []
    for day in menujson['jdata']:
        if day['ddate'] == date:
            menu = [day['line1'], day['line2'], day['line3']]
            break

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek", "corvin"],
    name='KAJAHU',
    id='kjh',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[]
)
