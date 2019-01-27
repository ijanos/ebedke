from datetime import timedelta
from provider.utils import get_dom, on_workdays

URL = "https://opusjazzclub.hu/etlap"

hungarian_month = {
    1: "jan",
    2: "febr",
    3: "márc",
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

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = f"{today.year}.{hungarian_month[today.month]}.{today.day:02}"
    menu = dom.xpath(f"//div[contains(@class, 'dailymenudish') and contains(preceding-sibling::div, '{ date }')]//text()")
    menu = list(dish.strip() for dish in menu)

    return menu

menu = {
    'name': 'Opus',
    'id': 'op',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=18),
    'cards': ['szep']
}
