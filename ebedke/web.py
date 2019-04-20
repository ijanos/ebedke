from datetime import datetime as dt
import json

import redis
from flask import Flask, jsonify, render_template, request

from ebedke.utils.utils import days_lower
from ebedke import pluginmanager
from ebedke.connections import redis

places = pluginmanager.load_plugins()

app = Flask(__name__, static_url_path='')
app.config.update(
    JSON_AS_ASCII=False,
    JSONIFY_MIMETYPE="application/json; charset=utf-8"
)

def cafeteriacard(cardname):
    tooltip = {
        "szep": "SZÉP-kártya elfogadóhely",
        "erzs": "Erzsébet kártya elfogadóhely"
    }
    return {
        "name": cardname,
        "tooltip": tooltip[cardname]
    }


def load_menus(restaurants):
    menus = zip(restaurants, redis.mget(f"{place.id}:menu" for place in restaurants))
    out = [{"name": place.name,
            "url": place.url,
            "id": place.id,
            "menu": json.loads(menu),
            "cards": map(cafeteriacard, place.cards)
            } for place, menu in menus]

    return out


def load_subdomain_menu():
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
                "cards": [card['name'] for card in menu['cards']]
                } for menu in load_menus(restaurants)]

    return jsonify(jsonout)

@app.route('/menu.json')
def api_v1():
    restaurants, _ = load_subdomain_menu()

    jsonout = [{"name": menu['name'],
                "url": menu['url'],
                "menu": menu['menu'],
                "cards": [card['name'] for card in menu['cards']]
                } for menu in load_menus(restaurants)]

    return jsonify(jsonout)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
