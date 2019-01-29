from datetime import timedelta

from provider.utils import get_dom, on_workdays

URL = "http://vegalife.hu/index.php?pc=webshop"

@on_workdays
def getMenu(today):
    dom = get_dom(URL, force_utf8=True)
    weekday = today.isoweekday()
    week = today.isocalendar()[1]
    items = dom.xpath(f'/html/body//table[@id="week_{week:02d}"]//tr//td[{weekday + 1}]//div[@class="meal"]/h4/text()')
    menu = list(line.strip() for line in items)
    return menu

menu = {
    'name': 'VegaLife',
    'id': 'vegalife',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['szep']
}
