import urllib
import urllib.request
from datetime import datetime

URL = "http://www.subway.hu/hu/page_menu_SOTD.html"
IMAGE_URL = "http://www.subway.hu/images/menu/WEB_NYITO_SOTD_644x360px.jpg"
EXPECTED_CONTENT_LENGTH = "418570"

foodMap = {
    0: "Roston sült csirke", # monday
    1: "Olasz fűszeres",
    2: "Sonka",
    3: "B.L.T.",
    4: "Falafel",
    5: "Omlett & Bacon",
    6: "Italian B.M.T." # sunday
}

def getMenu(today):
    # We trust that the foodMap is up-to-date if the image URL & size did not change
    with urllib.request.urlopen(urllib.request.Request(IMAGE_URL, method="HEAD")) as response:
        if response.getheader('content-length') == EXPECTED_CONTENT_LENGTH:
            menu = foodMap[today.weekday()] + " (Sub of the Day)"
        else:
            menu = 'Cache outdated. Please visit <a href="http://www.subway.hu/">http://www.subway.hu/</a> !'

        return {
            'name': 'Subway',
            'url': URL,
            'menu': menu
        }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
