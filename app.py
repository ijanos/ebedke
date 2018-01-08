from datetime import datetime as dt, timedelta
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import sys

import redis
from flask import Flask, jsonify, render_template

from provider import (pqs, kompot, bridges, tenminutes, opus, burgerking,
                      subway, dezso, manga, intenzo, golvonal, gilice, veranda,
                      portum, muzikum, amici, foodie, emi)

import config
from provider.utils import days_lower

MENU_ORDER = [
    bridges,
    pqs,
    kompot,
    gilice,
    tenminutes,
    dezso,
    amici,
    veranda,
    golvonal,
    portum,
    foodie,
    emi,
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

cache = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def load_menu(args):
    menu, today = args
    try:
        m = cache.get(menu['name'])
        while m is None:
            if cache.set(f"{menu['name']}:lock", 1, ex=20, nx=True):
                m = menu['get'](today)
                if not m:
                    cache.set(menu['name'], '', ex=14 * 60)
                else:
                    seconds_to_midnight = (23 - today.hour) * 3600 + (60 - today.minute) * 60
                    ttl = min(menu['ttl'].seconds, seconds_to_midnight)
                    cache.set(menu['name'], m, ex=ttl)
                break
            sleep(0.1)
            m = cache.get(menu['name'])
    except:
        print(f"Exception when downloading { menu['get'].__module__ }\n\t{ sys.exc_info() }")
        m = ''
        cache.set(menu['name'], '', ex=14 * 60)

    return {
        "name": menu['name'],
        "url": menu['url'],
        "menu": m
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
