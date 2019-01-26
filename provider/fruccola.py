from datetime import timedelta
import requests


URL = "http://fruccola.hu/hu"
API = "http://fruccola.hu/admin/api/daily_menu"

def getMenu(today):
    date = today.strftime("%Y-%m-%d")
    menujson = requests.get(API).json()['3']
    if menujson["due_date"] == date:
        menu = "<br>".join([menujson['soup_hu'], menujson['dish_hu']])
    else:
        menu = ""
    return menu

menu = {
    'name': 'Fruccola',
    'id': 'frc',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': []
}
