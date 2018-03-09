import traceback
from datetime import datetime as dt, timedelta
from concurrent.futures import ThreadPoolExecutor, Future
from time import sleep, perf_counter
import sys


import redis
from flask import Flask, jsonify, render_template
from requests.exceptions import Timeout

from provider.utils import days_lower, normalize_menu
from provider import (kompot, bridges, tenminutes, opus, burgerking, subway,
                      dezso, manga, intenzo, golvonal, gilice, veranda, portum,
                      muzikum, amici, foodie, emi, stex, kerova, cbacorvin, dagoba, greenhouse)

import config

MENU_ORDER = [
    bridges,
    kompot,
    gilice,
    tenminutes,
    dezso,
    amici,
    kerova,
    dagoba,
    greenhouse,
    cbacorvin,
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

def menu_loader(menu, today):
    start = perf_counter()
    daily_menu = None
    while daily_menu is None:
        if cache.set(f"{menu['name']}:lock", 1, ex=20, nx=True):
            try:
                daily_menu = menu['get'](today)
            except Timeout:
                print(f"[ebedke] timeout in «{menu['name']}» provider")
                daily_menu = ""
            except:
                print("[ebedke] exception:\n", traceback.format_exc())
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
    elapsed = perf_counter() - start
    print(f"[ebedke] loading «{menu['name']}» took {elapsed} seconds")
    return daily_menu


def load_menus(today):
    if config.OFFSET:
        today = today + timedelta(days=config.OFFSET)

    with ThreadPoolExecutor(max_workers=config.POOL_SIZE) as executor:
        menus = [(provider,
                  executor.submit(menu_loader, provider.menu, today) if menu is None else menu)
                 for provider, menu in
                 zip(MENU_ORDER,
                     cache.mget(provider.menu['name'] for provider in MENU_ORDER))
                ]

    return [{"name": provider.menu['name'],
             "url": provider.menu['url'],
             "menu": menu.result() if isinstance(menu, Future) else menu,
             "cards": provider.menu.get('cards', [])
            } for provider, menu in menus]

@app.route('/')
def root():
    today = dt.today()
    date = {
        'day': days_lower[today.weekday()],
        'date': today.strftime("%Y. %m. %d.")
    }
    return render_template("index.html", menus=load_menus(today), date=date, infobox=config.INFOBOX)

@app.route('/menu')
def dailymenu():
    return jsonify(list(load_menus(dt.today())))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        provider = sys.argv[1]
        offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        print(globals()[provider].menu['get'](dt.today() + timedelta(days=offset)))
    else:
        app.run(debug=True, use_reloader=True, host='0.0.0.0')
