from datetime import datetime as dt
import json

import redis
from flask import Flask, jsonify, render_template, request

from provider.utils import days_lower
from provider import *
import config

places = {
    "corvin": [tenminutes, tacsko, cbacorvin, dagoba, dezso, emi,
               foodie, gilice, golvonal, greenhouse, input, intenzo,
               joasszony, kerova, kompot, manga, muzikum, opus,
               portum, pqs, seastars, stex, veranda, zappa],

    "ferenciek": [fruccola, homefield, kajahu],

    "moricz": [keg, semmiextra, szatyor],

    "szepvolgyi": [officebistro, semmiextra, wasabi],

    "szell": [bocelli, ezisbudai, jegkert, joasszony, kbarcelona, pastafresca, vanbisztro],

    "default": [tenminutes, tacsko, bocelli, cbacorvin, dagoba, dezso, emi, ezisbudai, foodie, fruccola, gilice, golvonal,
                greenhouse, homefield, input, intenzo, jegkert, joasszony, kajahu, keg, kerova, kompot, kbarcelona, manga, muzikum,
                officebistro, opus, pastafresca, portum, pqs, semmiextra, seastars, stex, szatyor, vanbisztro, veranda,
                wasabi, zappa]
}

app = Flask(__name__, static_url_path='')
app.config.update(
    JSON_AS_ASCII=False
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
        restaurants = places['default']
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
