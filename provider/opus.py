from provider.utils import get_dom

URL = "http://opusjazzclub.hu/napimenu"

def getMenu(today):
    day = today.weekday()
    menu = ''
    try:
        dom = get_dom(URL)
        dayname = {
            0: "Hétfő",
            1: "Kedd",
            2: "Szerda",
            3: "Csütörtök",
            4: "Péntek"
        }
        if day in dayname:
            menu = dom.xpath('//div[@id="hetimenu"]//'
                            f'div[contains(text(),"{ dayname[day] }")]/'
                             'following-sibling::div[position() >= 1 and position() < 4]'
                             '/div[@class="etel_title_2" and string-length(normalize-space(text())) > 0]')
            menu = "<br>".join(div.text_content().strip() for div in menu)
    except:
        pass

    return {
        'name': 'Opus',
        'url': URL,
        'menu': menu
    }

if __name__ == "__main__":
    import datetime
    print(getMenu(datetime.datetime.today()))
