import json
import urllib.parse
import urllib.request
from lxml import html
from datetime import datetime


URL = "http://bridges.hu/#heti-menu"

def getMenu(today):
    day = today.weekday() + 1
    with urllib.request.urlopen(URL) as response:
        r = response.read()
        tree = html.fromstring(r)
        try:
            weekly_menu = tree.xpath('//*[@id="heti-menu"]//p')
            menu = weekly_menu[day].text_content()
            menu = menu + '<br>' + weekly_menu[6].text_content()
        except:
            menu = '-'

    return {
        'name': 'Bridges',
        'url':URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
