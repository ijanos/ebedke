import urllib.request
from lxml import html


URL = "http://verandaetterem.hu/"

def getMenu(today):
    day = today.weekday() + 2
    with urllib.request.urlopen(URL) as response:
        r = response.read()
        tree = html.fromstring(r)
        try:
            tds = tree.xpath(f'//div[@id="main-content"]//table[1]//tr[position() > 1 and position() < 6]/td[{ day }]')
            menu = "<br>".join(td.text_content().strip() for td in tds)
        except:
            menu = '-'

        return {
            'name': 'Veranda',
            'url': URL,
            'menu': menu
        }

if __name__ == "__main__":
    from datetime import datetime
    print(getMenu(datetime.today()))
