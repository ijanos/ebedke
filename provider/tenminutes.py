URL = "http://www.10minutes.hu/"

def getMenu(_):
    return {
        'name': '10 minutes',
        'url' : URL,
        'menu': '<img style="width: 100%; max-width:600px" src="http://www.10minutes.hu/images/home_1_06.png" />'
    }

if __name__ == "__main__":
    print(getMenu(None))
