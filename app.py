import traceback
from datetime import datetime as dt, timedelta
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import sys

import redis
from flask import Flask, jsonify, render_template

from provider.utils import days_lower, normalize_menu
from provider import (kompot, bridges, tenminutes, opus, burgerking, subway,
                      dezso, manga, intenzo, golvonal, gilice, veranda, portum,
                      muzikum, amici, foodie, emi, stex, kerova)

import config

MENU_ORDER = [
    bridges,
    kompot,
    gilice,
    tenminutes,
    dezso,
    amici,
    kerova,
    veranda,
    portum,
    foodie,
    emi,
    stex,
    golvonal,
    opus,
    manga,
    intenzo,
    muzikum,
    burgerking,
    subway
]

app = Flask(__name__, static_url_path='')
app.config.update(
    JSON_AS_ASCII=False,
    JSONIFY_PRETTYPRINT_REGULAR=False
)

cache = redis.StrictRedis(host=config.REDIS_HOST,
                          port=config.REDIS_PORT,
                          decode_responses=True)

def load_menu(args):
    menu, today = args
    daily_menu = cache.get(menu['name'])
    while daily_menu is None:
        if cache.set(f"{menu['name']}:lock", 1, ex=20, nx=True):
            try:
                daily_menu = menu['get'](today)
            except:
                print(traceback.format_exc())
                daily_menu = ""
            daily_menu = normalize_menu(daily_menu)
            if daily_menu is not "":
                seconds_to_midnight = (23 - today.hour) * 3600 + (60 - today.minute) * 60
                ttl = min(int(menu['ttl'].total_seconds()), seconds_to_midnight)
            else:
                ttl = 15 * 60
            cache.set(menu['name'], daily_menu, ex=ttl)
        else:
            sleep(0.05)
            daily_menu = cache.get(menu['name'])

    return {
        "name": menu['name'],
        "url": menu['url'],
        "menu": daily_menu
    }


def load_menus(today):
    if config.OFFSET:
        today = today + timedelta(days=config.OFFSET)
    with ThreadPoolExecutor(max_workers=config.POOL_SIZE) as executor:
        return executor.map(load_menu, [(r.menu, today) for r in MENU_ORDER])

@app.route('/')
def root():
    today = dt.today()
    date = {}
    date['day'] = days_lower[today.weekday()]
    date['date'] = today.strftime("%Y. %m. %d.")
    return render_template("index.html", menus=load_menus(today), date=date)

@app.route('/menu')
def dailymenu():
    return jsonify(list(load_menus(dt.today())))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
