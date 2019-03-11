#!/usr/bin/env python3

import json
import traceback
from time import sleep, perf_counter
from datetime import datetime as dt, timedelta
from collections.abc import Iterable

import redis
from requests.exceptions import Timeout

from utils.text import normalize_menu
import config
import ebedke

redis = redis.StrictRedis(host=config.REDIS_HOST,
                          port=config.REDIS_PORT)


DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"


def update(place, now):
    try:
        daily_menu = place.downloader(now)
        assert isinstance(daily_menu, Iterable), "Download function must return a list or other iteratable"
        daily_menu = normalize_menu(daily_menu)
    except Timeout:
        print(f"timeout in «{place.id}» provider")
        daily_menu = []
    except:
        print(f"exception in «{place.name}» provider:\n", traceback.format_exc())
        daily_menu = []

    redis.mset({
        f"{place.id}:menu": json.dumps(daily_menu),
        f"{place.id}:timestamp": now.strftime(DATEFORMAT)
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
    print(f"Updating «{place.name}»")
    start = perf_counter()
    update(place, now)
    elapsed = perf_counter() - start
    print(f"Updating «{place.name}» took {elapsed} seconds")


def loop(restaurantlist, must_update=False):
    now = dt.today()
    wait = waittime(now)

    if not must_update and now.hour >= 13:
        return

    for place in restaurantlist:
        menu, timestamp = redis.mget(f"{place.id}:menu",
                                     f"{place.id}:timestamp")
        if not timestamp:
            timestamp = dt.utcfromtimestamp(0)
        else:
            timestamp = dt.strptime(timestamp.decode("utf-8"), DATEFORMAT)

        menu_empty = menu == b"[]" or menu is None
        timestamp_is_today = timestamp.date() == now.date()
        timestamp_age = now - timestamp

        if not timestamp_is_today:
            do_update(place, now)
        elif timestamp_age > place.ttl:
            do_update(place, now)
        elif menu_empty and timestamp_age > wait:
            do_update(place, now)

if __name__ == "__main__":
    restaurantlist = ebedke.load_plugins()["all"]
    first_loop = True
    while True:
        print("starting update loop")
        loop(restaurantlist, must_update=first_loop)
        print("ending update loop")
        first_loop = False
        sleep(25)
