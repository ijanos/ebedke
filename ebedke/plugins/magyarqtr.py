from datetime import timedelta
from ebedke.utils.utils import get_dom, on_workdays, days_lower_ascii, pattern_slice
from ebedke.utils.text import remove_accents
from ebedke.pluginmanager import EbedkePlugin


URL = "http://www.magyarqtr.com/index.php?option=com_k2&view=item&layout=item&id=13&Itemid=231&lang=hu"


@on_workdays
def get_menu(today):
    dom = get_dom(URL)
    menu_week_number = dom.xpath("/html/body//div[@class='itemBody']//h2[@class='itemTitle']//text()")
    menu_week_number =  ''.join(char for char  in ''.join(menu_week_number) if char.isnumeric())
    _, current_week_number, _ = today.date().isocalendar()

    if menu_week_number == str(current_week_number):
        week_menu = dom.xpath("/html/body//div[@class='itemBody']//div[@class='heti-menu']//text()")
        lower = lambda line: remove_accents(line).lower()
        menu = pattern_slice(week_menu, [days_lower_ascii[today.weekday()]], days_lower_ascii, modifier=lower)
    else:
        menu = []

    return menu


plugin = EbedkePlugin(
    enabled=True,
    groups=["ferenciek"],
    name="MagyarQTR",
    id="mqtr",
    url=URL,
    downloader=get_menu,
    ttl=timedelta(hours=24),
    cards=[]
)
