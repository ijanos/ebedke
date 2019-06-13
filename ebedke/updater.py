#!/usr/bin/env python3

import json
import traceback
from time import sleep, perf_counter
from typing import List, Dict, Union
from datetime import datetime as dt, time, timedelta
from requests.exceptions import Timeout

from ebedke.utils.text import normalize_menu
from ebedke.connections import redis
from ebedke.utils import cache
from ebedke import pluginmanager

DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"

# pylint: disable=bare-except
def update(place: pluginmanager.EbedkePlugin, now: dt) -> None:
    daily_menu: List[str]
    try:
        daily_menu = place.downloader(now)
        daily_menu = normalize_menu(daily_menu)
    except Timeout:
        print(f"timeout in «{place.name}» provider")
        daily_menu = []
    except:
        print(f"exception in «{place.name}» provider:\n", traceback.format_exc())
        daily_menu = []

    menu = {
        "menu": daily_menu,
        "timestamp": now.strftime(DATEFORMAT)
    }

    redis.set(
        name=f"{place.id}:menu",
        value=json.dumps(menu),
        ex=86400 # 24 hours
    )


def get_refresh_time(date: dt) -> timedelta:
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
    else:
        wait = minutes(60)
    return wait


def do_update(place: pluginmanager.EbedkePlugin, now: dt) -> None:
    start = perf_counter()
    update(place, now)
    elapsed = perf_counter() - start
    print(f"Updated «{place.name}» in {elapsed:.2f} seconds")


def update_restaurants(restaurantlist: List[pluginmanager.EbedkePlugin], now: dt) -> None:
    refresh_time = get_refresh_time(now)
    parsed_menu_list: List[Dict[str, Union[str, List[str]]]] = cache.get_menu(restaurantlist)
    for i, place in enumerate(restaurantlist):
        current_menu = parsed_menu_list[i]

        current_timestamp = current_menu.get("timestamp")
        timestamp: dt = dt.strptime(current_timestamp, DATEFORMAT) \
            if isinstance(current_timestamp, str) else dt.utcfromtimestamp(0)

        cached_menu = current_menu.get("menu", [])
        menu: List[str] = cached_menu if isinstance(cached_menu, list) else []
        menu_empty = not menu
        timestamp_is_today = timestamp.date() == now.date()
        timestamp_age = now - timestamp
        refreshable = timestamp_age > refresh_time

        empty_expired = menu_empty and refreshable
        expired = not timestamp_is_today or (timestamp_age > place.ttl and refreshable)

        if empty_expired or expired:
            do_update(place, now)

def main_loop() -> None:
    restaurantlist = pluginmanager.load_plugins()["all"]
    first_loop = True

    while True:
        now = dt.today()
        if first_loop or now.time() < time(12, 40):
            update_restaurants(restaurantlist, now)

        first_loop = False
        sleep(20)


if __name__ == "__main__":
    main_loop()
