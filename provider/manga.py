from datetime import datetime as dt, timedelta
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

    return menu

menu = {
    'name': 'Manga',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=5)
}

if __name__ == "__main__":
    print(getMenu(dt.today()))
