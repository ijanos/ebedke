import urllib.request
from lxml import html


URL = "http://dezsoba.hu/hu/heti-menue"

def getMenu(today):
    day = today.weekday()
    with urllib.request.urlopen(URL) as response:
        r = response.read()
        tree = html.fromstring(r)
        menu = tree.xpath('//div[@class="sppb-menu-text"]')
        try:
            menu = '<br>'.join(menu[day].xpath("text()"))
        except:
            menu = '-'

        return {
            'name': 'Dezső bá',
            'url': URL,
            'menu': menu
        }

if __name__ == "__main__":
    import datetime
    print(getMenu(datetime.datetime.today()))
