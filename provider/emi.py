from datetime import timedelta
from provider.utils import get_dom, on_workdays

URL = "http://www.emikifozte.hu/menuk.php"

@on_workdays
def getMenu(_):
    dom = get_dom(URL)
    menu = dom.xpath('/html/body//tr[@class="menutablasor"]/td[3]')
    menu = '<br>'.join(e.text_content().strip('(, )') for e in menu)

    return menu

menu =  {
    'name': 'Emi kifőzte',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(minutes=25),
    'cards': ['szep', 'erzs']
}
