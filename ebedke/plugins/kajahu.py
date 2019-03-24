from datetime import timedelta
from ebedke.utils.utils import on_workdays, http_get
from ebedke.pluginmanager import EbedkePlugin


URL = "https://www.kajahu.com/etlap/d"
API = "https://appif.kajahu.com/jdmenu?jlang=hu&jseat=-"


@on_workdays
def getMenu(today):
    date = today.strftime("%Y-%m-%d")
    menujson = http_get(API).json()
    menu = []
    for day in menujson['jdata']:
        if day['ddate'] == date:
            menu = [day['line1'], day['line2'], day['line3']]
            break

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name='KAJAHU',
    id='kjh',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[]
)
