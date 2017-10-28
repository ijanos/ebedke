URL = "http://netpincer.hu"

def getMenu(today):
    if today.weekday() > 4:
        return {
            'name': 'Netpincér',
            'url': URL,
            'menu': "Hétvége van, rendelj pizzát ;)"
        }
    else:
        return None

if __name__ == "__main__":
    import datetime
    print(getMenu(datetime.datetime.today()))
