from datetime import datetime as dt
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
from provider import manga
from provider import intenzo
from provider import golvonal
from provider import gilice
from provider import veranda

FOODSOURCES = [
    bridges,
    pqs,
    kompot,
    gilice,
    tenminutes,
    dezso,
    veranda,
    golvonal,
    opus,
    manga,
    intenzo,
    burgerking,
    subway
]

def menuLoader(getMenu):
    today = dt.today()
    if config.OFFSET:
        from datetime import timedelta
        today = today + timedelta(days=config.OFFSET)
    menu = getMenu(today)
    return menu

def getDailyMenuParallel():
    with Pool(config.POOL_SIZE) as pool:
        all_menu = pool.map(menuLoader, [r.getMenu for r in FOODSOURCES])
    return all_menu

if __name__ == "__main__":
    print(getDailyMenuParallel())
