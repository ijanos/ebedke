import locale
from provider.utils import get_dom

URL = "https://opusjazzclub.hu/etlap"

def getMenu(today):
    menu = ''
    try:
        dom = get_dom(URL)
        locale.setlocale(locale.LC_TIME, "hu_HU.UTF-8")
        date = today.strftime("%Y.%b.%d.").lower()
        menu = dom.xpath(f"//div[contains(@class, 'dailymenudish') and contains(preceding-sibling::div, '{ date }')]//text()")
        menu = "<br>".join(dish.strip() for dish in menu)
    except:
        pass

    return {
        'name': 'Opus',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    import datetime
    from datetime import timedelta
    print(getMenu(datetime.datetime.today()))
