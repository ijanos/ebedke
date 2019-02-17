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

def loop(restaurantlist):
    now = dt.today()
    wait = waittime(now)

    for r in restaurantlist:
        menu, timestamp = redis.mget(f"{r.menu['id']}:menu", f"{r.menu['id']}:timestamp")
        if not timestamp:
            timestamp = dt.utcfromtimestamp(0)
        else:
            timestamp = dt.strptime(timestamp.decode("utf-8"), DATEFORMAT)

        do_update = False
        if timestamp.date() != now.date():
            do_update = True
        elif now - timestamp > r.menu['ttl'] and menu != b"[]":
            do_update = True
        elif menu == b"[]" and now - timestamp > wait:
            do_update = True

        if do_update:
            print(f"Updating «{r.menu['name']}»")
            start = perf_counter()
            update(r.menu['id'], r.menu['get'], now)
            elapsed = perf_counter() - start
            print(f"Updating «{r.menu['name']}» took {elapsed} seconds")

if __name__ == "__main__":
    restaurantlist = restaurants.places['all']
    while True:
        print("starting update loop")
        loop(restaurantlist)
        print("ending update loop")
        sleep(20)
