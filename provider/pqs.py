import urllib.request
from lxml import html


PQS_MENU = "http://pqs.hu/hu/etlapok?e=56"

def getMenu(today):
    day = today.weekday() + 1
    with urllib.request.urlopen(PQS_MENU) as response:
        r = response.read()
        tree = html.fromstring(r)
        cells = [2, 4, 6, 26, 28, 30]
        try:
            menu = ""
            for cell in cells:
                ul = tree.xpath(f'//*[@id="menu"]/tbody/tr[{cell}]/td[{day}]/ul')[0]
                menu += ul.text_content().strip() + '<br>'
            menu = menu.replace("Választott leves","")
        except:
            menu = '-'

        return {
            'name': 'PQS Skypark',
            'url': PQS_MENU,
            'menu': menu
        }

if __name__ == "__main__":
    from datetime import datetime
    print(getMenu(datetime.today()))
