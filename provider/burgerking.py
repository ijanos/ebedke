from provider.utils import content_size_match

URL = "http://burgerking.hu/offers"
IMG_URL = "http://burgerking.hu/sites/burgerking.hu/files/HetkozNapiBKmenu_Mindentermek_lista_1000x550px.jpg"

burgerking_menu = {
    0: "Whopper",
    1: "Big King",
    2: "Western Whopper",
    3: "Whopper",
    4: "Deluxe csirkemell"
}

def getMenu(today):
    day = today.weekday()
    IMG_SIZE = "181621"
    if content_size_match(IMG_URL, IMG_SIZE) and day < 5:
        menu = burgerking_menu[day]
    else:
        menu = ''

    return {
        'name': 'Burger King',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    from datetime import datetime
    print(getMenu(datetime.today()))
