from datetime import datetime as dt
from typing import List, Dict, Tuple, Sequence
from flask import Flask, jsonify, render_template, request

from ebedke.utils.date import days_lower
import ebedke.utils.cache as cache
from ebedke import pluginmanager


places = pluginmanager.load_plugins()

app = Flask(__name__, static_url_path='')
app.config.update(
    JSON_AS_ASCII=False,
    JSONIFY_MIMETYPE="application/json; charset=utf-8"
)

def cafeteriacard(cardname: str) -> Dict[str, str]:
    tooltip = {
        "szep": "SZÉP-kártya elfogadóhely",
        "erzs": "Erzsébet kártya elfogadóhely"
    }
    return {
        "name": cardname,
        "tooltip": tooltip[cardname]
    }


def load_menus(restaurants: List[pluginmanager.EbedkePlugin]) -> List[Dict[str, object]]:
    parsed_menu_list = cache.get_menu(restaurants)
    result = []
    for i, place in enumerate(restaurants):
        menu: Sequence[str] = parsed_menu_list[i].get("menu", [])
        result.append({
            "name": place.name,
            "url": place.url,
            "id": place.id,
            "menu": menu,
            "cards": list(map(cafeteriacard, place.cards)),
            "coord": place.coord
        })
    return result


def load_subdomain_menu() -> Tuple[List[pluginmanager.EbedkePlugin], bool]:
    subdomain = request.host.split(".")[0]
    if subdomain in places:
        restaurants = places[subdomain]
        welcome = False
    else:
        restaurants = places['all']
        welcome = True
    return restaurants, welcome

@app.route('/')
def root():
    restaurants, welcome = load_subdomain_menu()
    today = dt.today()
    date = {
        'day': days_lower[today.weekday()],
        'date': today.strftime("%Y. %m. %d.")
    }
    return render_template("index.html", menus=load_menus(restaurants), date=date, welcome=welcome)

@app.route('/menu')
def dailymenu():
    restaurants, _ = load_subdomain_menu()

    jsonout = [{"name": menu['name'],
                "url": menu['url'],
                "menu": '<br>'.join(menu['menu']),
                "cards": [card['name'] for card in menu['cards']],
                "coord": menu['coord']
                } for menu in load_menus(restaurants)]

    return jsonify(jsonout)

@app.route('/menu.json')
def api_v1():
    restaurants, _ = load_subdomain_menu()

    jsonout = [{"name": menu['name'],
                "url": menu['url'],
                "menu": menu['menu'],
                "cards": [card['name'] for card in menu['cards']],
                "coord": menu['coord']
                } for menu in load_menus(restaurants)]

    return jsonify(jsonout)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
