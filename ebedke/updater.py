#!/usr/bin/env python3

import json
import traceback
from time import sleep, perf_counter
from datetime import datetime as dt, time, timedelta

import redis
from requests.exceptions import Timeout

from ebedke.utils.text import normalize_menu
from ebedke.connections import redis
from ebedke import pluginmanager

DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"

# pylint: disable=bare-except
def update(place, now):
    try:
        daily_menu = place.downloader(now)
        daily_menu = normalize_menu(daily_menu)
    except Timeout:
        print(f"timeout in «{place.name}» provider")
        daily_menu = []
    except:
        print(f"exception in «{place.name}» provider:\n", traceback.format_exc())
        daily_menu = []

    redis.mset({
        f"{place.id}:menu": json.dumps(daily_menu),
        f"{place.id}:timestamp": now.strftime(DATEFORMAT)
    })


def get_refresh_time(date):
    minutes = lambda n: timedelta(minutes=n)
    now = date.time()
    if now < time(8, 00):
        wait = minutes(120)
    elif now < time(10, 00):
        wait = minutes(20)
    elif now < time(11, 00):
        wait = minutes(10)
    elif now < time(13, 00):
        wait = minutes(5)
    return wait


def do_update(place, now):
    start = perf_counter()
    update(place, now)
    elapsed = perf_counter() - start
    print(f"Updated «{place.name}» in {elapsed:.2f} seconds")


def update_restaurants(restaurantlist, now):
    refresh_time = get_refresh_time(now)
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
        refreshable = timestamp_age > refresh_time

        empty_expired = menu_empty and refreshable
        expired = not timestamp_is_today or (timestamp_age > place.ttl and refreshable)

        if empty_expired or expired:
            do_update(place, now)

def main_loop():
    restaurantlist = pluginmanager.load_plugins()["all"]
    first_loop = True

    while True:
        now = dt.today()
        if first_loop or now.time() < time(13, 00):
            update_restaurants(restaurantlist, now)

        first_loop = False
        sleep(20)


if __name__ == "__main__":
    main_loop()
