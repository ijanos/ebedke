import urllib.request
from lxml import html


URL = "http://mangacowboy.hu/"

def getMenu(today):
    day = today.weekday()
    with urllib.request.urlopen(URL) as response:
        r = response.read()
        tree = html.fromstring(r)
        menu = tree.xpath('//*[@id="weekly_menu"]//div[@class="weeklyMenuPreview-content"]')
        try:
            menu = '<br>'.join(menu[day].xpath("p/text()"))
        except:
            menu = '-'

        return {
            'name': 'Manga',
            'url': URL,
            'menu': menu
        }

if __name__ == "__main__":
    import datetime
    print(getMenu(datetime.datetime.today()))
