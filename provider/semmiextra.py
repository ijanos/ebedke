from datetime import timedelta
from provider.utils import get_dom, skip_empty_lines, on_workdays


URL = "http://semmiextra.hu/bartok-bela-ut-etterem#heti-menu"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    menu = dom.xpath("/html/body//div[@id='heti-menu']//ul[@class='dotted']/li/text()")
    menu = '<br>'.join(skip_empty_lines(menu))

    return menu

menu = {
    'name': 'Semmi Extra',
    'id': 'se',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=4),
    'cards': ['erzs']
}
