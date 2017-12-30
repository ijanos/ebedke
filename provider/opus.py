from provider.utils import get_dom

URL = "https://opusjazzclub.hu/etlap"

hungarian_month = {
    1: "jan",
    2: "feb",
    3: "már",
    4: "ápr",
    5: "máj",
    6: "jún",
    7: "júl",
    8: "aug",
    9: "szept",
    10: "okt",
    11: "nov",
    12: "dec"
}

def getMenu(today):
    menu = ''
    try:
        dom = get_dom(URL)
        date = f"{ today.year }.{ hungarian_month[today.month] }.{today.day:02}"
        menu = dom.xpath(f"//div[contains(@class, 'dailymenudish') and contains(preceding-sibling::div, '{ date }')]//text()")
        menu = "<br>".join(dish.strip() for dish in menu)
        if "nincs menü" in menu.lower():
            menu = ""
    except:
        pass

    return {
        'name': 'Opus',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    import datetime
    print(getMenu(datetime.datetime.today()))
