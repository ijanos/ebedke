from datetime import datetime, timedelta
from provider.utils import content_size_match

URL = "http://www.subwayhungary.com/hu/page_menu_SOTD.html"
IMAGE_URL = "https://www.subwayhungary.com/images/menu/WEB_NYITO_SOTD_644x360.jpg"
EXPECTED_CONTENT_LENGTH = "1511684"

foodMap = {
    0: "Csirke", # monday
    1: "Olasz fűszeres",
    2: "Sonka",
    3: "B.L.T.",
    4: "Falafel",
    5: "Omlett & Bacon",
    6: "Big Beef Melt" # sunday
}

def getMenu(today):
    if content_size_match(IMAGE_URL, EXPECTED_CONTENT_LENGTH):
        menu = foodMap[today.weekday()] + " (Sub of the Day)"
    else:
        menu = 'Tekintse meg a <a href="' + URL + '">Subway honlapján</a>!'

    return menu

menu = {
    'name': 'Subway',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=14),
    'cards': ['szep', 'erzs']
}
