import json
from ebedke.connections import redis

def get_menu(restaurantlist):
    raw_menu_list = redis.mget(f"{place.id}:menu" for place in restaurantlist)
    return [json.loads(m) if m else {} for m in raw_menu_list]
