from datetime import timedelta
import requests


URL = "http://fruccola.hu/hu"
API = "http://fruccola.hu/admin/api/daily_menu"

def getMenu(today):
    date = today.strftime("%Y-%m-%d")

    menu = ""
    for menu in requests.get(API).json().values():
        if menu['place_id'] == 2 and menu["due_date"] == date:
            menu = "<br>".join([menu['soup_hu'], menu['dish_hu']])
            break

    return menu

menu = {
    'name': 'Fruccola (Kristóf tér)',
    'id': 'frc',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['szep']
}
