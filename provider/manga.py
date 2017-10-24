from datetime import datetime as dt
from provider.utils import get_dom


URL = "http://mangacowboy.hu/"

def getMenu(today):
    try:
        dom = get_dom(URL)
        date = today.strftime("%Y. %m. %d.")
        menu = dom.xpath(f'//section[@id="weekly_menu"]/ul/li[.//time[contains(text(), "{ date }")]]'
                            '//div[@class="weeklyMenuPreview-content"]')
        menu = '<br>'.join(menu[0].xpath("./p/text()"))
    except:
        menu = ''

    return {
        'name': 'Manga',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(dt.today()))
