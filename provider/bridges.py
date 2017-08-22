import urllib.parse
import urllib.request
from datetime import timedelta, datetime

from lxml import html


URL = "http://bridges.hu/#heti-menu"

def getMenu(today):
    day = today.weekday() + 1
    with urllib.request.urlopen(URL) as response:
        r = response.read()
        tree = html.fromstring(r)
        menu = '-'
        try:
            weekly_menu = tree.xpath('//*[@id="heti-menu"]//p')
            date = weekly_menu[0].text_content().strip()[0:10]
            parse_date = lambda d: datetime.strptime(d, '%Y.%m.%d').date()
            if parse_date(date) > today.date() - timedelta(days=6):
                menu = weekly_menu[day].text_content()
                menu = menu.replace('1.', '<br>1.')
                menu = menu.replace('2.', '<br>2.')
                menu = menu + '<br>' + weekly_menu[6].text_content()
        except:
            pass

    return {
        'name': 'Bridges',
        'url':URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
