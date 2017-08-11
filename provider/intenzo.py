import urllib.request
from lxml import html


URL = "http://cafeintenzo.hu/#hetimenu"

def getMenu(today):
    day = today.weekday()
    with urllib.request.urlopen(URL) as response:
        r = response.read()
        tree = html.fromstring(r)
        menu = tree.xpath('//*[@id="hetimenu"]//div[contains(@class, "text_box")]')
        try:
            menu = '<br>'.join(menu[day].xpath("p/text()"))
        except:
            menu = '-'

        return {
            'name': 'Intenzo',
            'url': URL,
            'menu': menu
        }

if __name__ == "__main__":
    import datetime
    print(getMenu(datetime.datetime.today()))
