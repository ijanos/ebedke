import urllib.request
from lxml import html


URL = "http://www.golvonalbisztro.hu/heti-menuajanlat.html"

def getMenu(today):
    day = today.weekday()
    weekdays = {
        0: "HÉTFŐ",
        1: "KEDD",
        2: "SZERDA",
        3: "CSÜTÖRTÖK",
        4: "PÉNTEK"
    }
    with urllib.request.urlopen(URL) as response:
        r = response.read()
        tree = html.fromstring(r)
        try:
            menu = tree.xpath(f'//div[@class="fck"]//h3[contains(*[text()], "{ weekdays[day] }")]/following-sibling::p[position() >= 1 and position() < 3]')
            menu = '<br>'.join(p.text for p in menu)
        except:
            menu = '-'

        return {
            'name': 'Gólvonal',
            'url': URL,
            'menu': menu
        }

if __name__ == "__main__":
    import datetime
    print(getMenu(datetime.datetime.today()))
