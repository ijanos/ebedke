import json
from typing import List, Dict, Union
from ebedke.connections import redis
from ebedke import pluginmanager

def get_menu(restaurantlist: List[pluginmanager.EbedkePlugin]) -> List[Dict[str, Union[List[str], str]]]:
    raw_menu_list = redis.mget(f"{place.id}:menu" for place in restaurantlist)
    return [json.loads(m) if m else {} for m in raw_menu_list]
