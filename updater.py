#!/usr/bin/env python3

import json
import traceback
from time import sleep, perf_counter
from datetime import datetime as dt, timedelta

import redis
from requests.exceptions import Timeout

from provider import restaurants
from provider.utils import normalize_menu
import config

redis = redis.StrictRedis(host=config.REDIS_HOST,
                          port=config.REDIS_PORT)


DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"

def update(id, downloader, now):
    try:
        daily_menu = downloader(now)
        assert isinstance(daily_menu, list)
    except Timeout:
        print(f"timeout in «{id}» provider")
        daily_menu = []
    except:
        print(f"exception in «{id}» provider:\n", traceback.format_exc())
        daily_menu = []
    daily_menu = normalize_menu(daily_menu)

    redis.mset({
        f"{id}:menu": json.dumps(daily_menu),
        f"{id}:timestamp": now.strftime(DATEFORMAT)
    })

def waittime(date):
    if date.hour < 10:
        wait = timedelta(minutes=45)
    elif date.hour >= 10 and date.hour <= 12:
        wait = timedelta(minutes=5)
    else:
        wait = timedelta(minutes=150)
    return wait


def do_update(place, now):
    print(f"Updating «{place.menu['name']}»")
    start = perf_counter()
    update(place.menu['id'], place.menu['get'], now)
    elapsed = perf_counter() - start
    print(f"Updating «{place.menu['name']}» took {elapsed} seconds")


def loop(restaurantlist, must_update=False):
    now = dt.today()
    wait = waittime(now)

    if not must_update and now.hour >= 13:
        return

    for place in restaurantlist:
        menu, timestamp = redis.mget(f"{place.menu['id']}:menu",
                                     f"{place.menu['id']}:timestamp")
        if not timestamp:
            timestamp = dt.utcfromtimestamp(0)
        else:
            timestamp = dt.strptime(timestamp.decode("utf-8"), DATEFORMAT)

        menu_empty = menu == b"[]" or menu is None
        timestamp_is_today = timestamp.date() == now.date()
        timestamp_age = now - timestamp

        if not timestamp_is_today:
            do_update(place, now)
        elif timestamp_age > place.menu['ttl']:
            do_update(place, now)
        elif menu_empty and timestamp_age > wait:
            do_update(place, now)

if __name__ == "__main__":
    restaurantlist = restaurants.places['all']
    first_loop = True
    while True:
        print("starting update loop")
        loop(restaurantlist, must_update=first_loop)
        print("ending update loop")
        first_loop = False
        sleep(25)
