"""
This is a fake redis module for testing
"""
import json

DB = {}

def reset():
    DB = {}

def set(name, value, ex=0):
    DB[name] = value

def get(name):
    return DB.get(name, None)

def get_menu(restaurantlist):
    ret = []
    for place in restaurantlist:
        menu = get(f"{place.id}:menu")
        if menu:
            ret.append(json.loads(menu))
        else:
            ret.append({})
    return ret
