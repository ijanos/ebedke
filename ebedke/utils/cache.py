import sys
import json
from typing import List, Dict, Union
from ebedke.connections import redis, RedisConnectionError
from ebedke import pluginmanager

def get_menu(restaurantlist: List[pluginmanager.EbedkePlugin]) -> List[Dict[str, Union[List[str], str]]]: # pylint: disable=unsubscriptable-object
    try:
        raw_menu_list = redis.mget(f"{place.id}:menu" for place in restaurantlist)
    except RedisConnectionError:
        print("Redis connection error. Exiting.")
        sys.exit(1)

    return [json.loads(m) if m else {} for m in raw_menu_list]
