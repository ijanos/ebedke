from datetime import timedelta
from provider.utils import http_get


URL = "http://fruccola.hu/hu"
API = "http://fruccola.hu/admin/api/daily_menu"

def getMenu(today):
    date = today.strftime("%Y-%m-%d")

    out = []
    for place in http_get(API).json().values():
        if "place_id" in menu and menu['place_id'] == 2 and menu["due_date"] == date:
            out = [menu['soup_hu'], menu['dish_hu']]
            break

    return out

menu = {
    'name': 'Fruccola (Kristóf tér)',
    'id': 'frc',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['szep']
}
