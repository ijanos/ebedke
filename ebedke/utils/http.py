import pickle
from functools import partial
import requests
from lxml import html
from ebedke import connections, settings

def get(url, *, params=None, verify=True):
    headers = {
        'User-Agent': settings.user_agent,
    }
    req_get = partial(requests.get, headers=headers, params=params, timeout=10, verify=verify)

    if settings.debug_mode:
        cached = connections.redis.get(f"cache:{url}")
        if not cached:
            print("[ebedke] saving to redis cache")
            cached = req_get(url)
            connections.redis.set(f"cache:{url}", pickle.dumps(cached), ex=3600)
            response = cached
        else:
            print("[ebedke] loaded from redis cache")
            response = pickle.loads(cached)
    else:
        response = req_get(url)
    return response

def get_dom(url, force_utf8=False, verify=True):
    response = get(url, verify=verify)
    if force_utf8:
        response.encoding = 'utf-8'
    return html.fromstring(response.text)
