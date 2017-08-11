import json
import datetime
from multiprocessing import Pool

import config

from provider import pqs
from provider import kompot
from provider import bridges
from provider import tenminutes
from provider import opus
from provider import burgerking
from provider import subway
from provider import dezso

FOODSOURCES = [
    bridges,
    pqs,
    kompot,
    tenminutes,
    opus,
    dezso,
    burgerking,
    subway
]

def menuLoader(getMenu):
    today = datetime.datetime.today()
    return getMenu(today)

def getDailyMenu():
    all_menu = list(map(menuLoader, [r.getMenu for r in FOODSOURCES]))
    return all_menu

def getDailyMenu_parallel():
    with Pool(config.POOL_SIZE) as pool:
        print("downloading menu")
        all_menu = pool.map(menuLoader, [r.getMenu for r in FOODSOURCES])
        return all_menu

if __name__ == "__main__":
    print(getDailyMenu())
