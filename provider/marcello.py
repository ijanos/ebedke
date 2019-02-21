from datetime import timedelta
from provider.utils import get_dom, on_workdays, months_hu_capitalized

URL = "https://www.marcelloetterem.hu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = f"{today.month:02}.{today.day:02}"
    menu = dom.xpath(f"/html/body//div[.//a[contains(text(), '{date}')]]/p//text()")
    menu = [m.capitalize() for m in menu[:3]]
    return menu

menu = {
    'name': 'Marcello',
    'id': 'mrc',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=24),
    'cards': ["szep", "erzs"]
}
