from datetime import timedelta, time
from ebedke.pluginmanager import EbedkePlugin


test_menu_list = ["test menu line 1", "test menu line 2"]

def download_menu(today):
    if today.time() < time(8, 0):
        return []
    else:
        return test_menu_list

test_plugin1 = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='My Restaurant',
    id='test1',
    url="http://myrestarunt.myrestaruant",
    downloader=download_menu,
    ttl=timedelta(hours=24),
    cards=['szep'],
    coord=(47.5, 19)
)

test_plugin2 = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='My Restaurant 2',
    id='test2',
    url="http://myrestarunt.myrestaruant",
    downloader=download_menu,
    ttl=timedelta(minutes=20),
    cards=['szep'],
    coord=(47.5, 19)
)
