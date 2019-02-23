from datetime import datetime as dt
import json

import redis
from flask import Flask, jsonify, render_template, request

from provider.utils import days_lower
from provider import *
from provider import restaurants
import config

places = restaurants.places

app = Flask(__name__, static_url_path='')
app.config.update(
    JSON_AS_ASCII=False,
    JSONIFY_MIMETYPE="application/json; charset=utf-8"
)

cache = redis.StrictRedis(host=config.REDIS_HOST,
                          port=config.REDIS_PORT)

def cafeteriacard(cardname):
    tooltip = {
        "szep": "SZÉP-kártya elfogadóhely",
        "erzs": "Erzsébet kártya elfogadóhely"
    }
    return {
        "name": cardname,
        "tooltip": tooltip[cardname]
    }


def load_menus(today, restaurants):
    menus = zip(restaurants, cache.mget(f"{provider.menu['id']}:menu" for provider in restaurants))
    out = [{"name": provider.menu['name'],
            "url": provider.menu['url'],
            "id": provider.menu["id"],
            "menu": json.loads(menu),
            "cards": map(cafeteriacard, provider.menu.get('cards', []))
            } for provider, menu in menus]

    return out


def load_subdomain_menu():
    subdomain = request.host.split(".ebed.today")[0]
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
    return render_template("index.html", menus=load_menus(today, restaurants), date=date, welcome=welcome)

@app.route('/menu')
def dailymenu():
    restaurants, _ = load_subdomain_menu()

    jsonout = [{"name": menu['name'],
                "url": menu['url'],
                "menu": '<br>'.join(menu['menu']),
                "cards": [card['name'] for card in menu['cards']]
                } for menu in load_menus(dt.today(), restaurants)]

    return jsonify(jsonout)

@app.route('/menu.json')
def api_v1():
    restaurants, _ = load_subdomain_menu()

    jsonout = [{"name": menu['name'],
                "url": menu['url'],
                "menu": menu['menu'],
                "cards": [card['name'] for card in menu['cards']]
                } for menu in load_menus(dt.today(), restaurants)]

    return jsonify(jsonout)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
