import pickle
from functools import partial
import requests
from ebedke import connections
from ebedke import settings

def get(url, *, params=None, verify=True):
    headers = {
        'User-Agent': settings.user_agent,
    }
    get = partial(requests.get, headers=headers, params=params, timeout=10, verify=verify)

    if settings.debug_mode:
        cached = connections.redis.get(f"cache:{url}")
        if not cached:
            print("[ebedke] saving to redis cache")
            cached = get(url)
            connections.redis.set(f"cache:{url}", pickle.dumps(cached), ex=3600)
            response = cached
        else:
            print("[ebedke] loaded from redis cache")
            response = pickle.loads(cached)
    else:
        response = get(url)
    return response
