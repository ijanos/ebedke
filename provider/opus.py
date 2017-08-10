import urllib.request
from lxml import html


URL = "http://opusjazzclub.hu/napimenu"

def getMenu(today):
    day = today.weekday()
    with urllib.request.urlopen(URL) as response:
        r = response.read()
        tree = html.fromstring(r)
        dayname = {
            0: "Hétfő",
            1: "Kedd",
            2: "Szerda",
            3: "Csütörtök",
            4: "Péntek"
        }

        if day in dayname:
            menu = tree.xpath('//*[@id="hetimenu"]//'
                             f'div[contains(text(),"{dayname[day]}")]/'
                              'following-sibling::div[position() >= 1 and position() < 4]'
                              '/div[@class="etel_title_2" and string-length(normalize-space(text())) > 0]')
            menu = "<br>".join(div.text_content().strip() for div in menu)
        else:
            menu = '-'

        return {
            'name': 'Opus',
            'url': URL,
            'menu': menu
        }

if __name__ == "__main__":
    import datetime
    print(getMenu(datetime.datetime.today()))
