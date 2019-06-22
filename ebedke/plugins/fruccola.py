from typing import List

from datetime import timedelta
from ebedke.utils import http
from ebedke.pluginmanager import EbedkePlugin

URL = "http://fruccola.hu/hu"
API = "http://fruccola.hu/admin/api/daily_menu"

def getMenu(today):
    date = today.strftime("%Y-%m-%d")
    out: List[str] = []
    for place in http.get(API).json().values():
        if "place_id" in place and place['place_id'] == 2 and place["due_date"] == date:
            out = [place['soup_hu'], place['dish_hu']]
            break

    return out

plugin = EbedkePlugin(
    enabled=True,
    name='Fruccola (Kristóf tér)',
    id='frc',
    url=URL,
    downloader=getMenu,
    ttl=timedelta(minutes=60),
    cards=['szep'],
    groups=["ferenciek"]
)
