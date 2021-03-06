import sys
import pickle
from functools import partial
from datetime import datetime
from typing import Optional, Dict, Any
import requests
from lxml import html
from ebedke import settings
from ebedke.connections import redis, RedisConnectionError

def unsafe_get(url: str, *, params: Dict[str, Any] = None, verify: bool = True) -> requests.Response:
    headers = {
        'User-Agent': settings.user_agent,
    }
    req_get = partial(requests.get, headers=headers, params=params, timeout=10, verify=verify)

    if settings.debug_mode:
        pickled_cache = redis.get(f"cache:{url}")
        if not pickled_cache:
            print("[ebedke] saving to redis cache")
            response = req_get(url)
            redis.set(f"cache:{url}", pickle.dumps(response), ex=3600)
        else:
            print("[ebedke] loaded from redis cache")
            response = pickle.loads(pickled_cache)
    else:
        response = req_get(url)
    return response

def get(url: str, *, params: Dict[str, Any] = None, verify: bool = True) -> requests.Response:
    try:
        return unsafe_get(url, params=params, verify=verify)
    except RedisConnectionError:
        print("Redis connection error. Exiting.")
        sys.exit(1)

def get_dom(url: str, force_utf8: bool = False, verify: bool = True) -> html.HtmlElement:
    response = get(url, verify=verify)
    if force_utf8:
        response.encoding = 'utf-8'
    return html.fromstring(response.text)

def get_bytes(url: str) -> bytes:
    response = get(url)
    return response.content

def get_fresh_image(url: str, fresh_date: datetime) -> Optional[bytes]: # pylint: disable=unsubscriptable-object
    response = get(url)
    lastmod = response.headers.get('last-modified')
    if not lastmod:
        print("[ebedke] image is missing last-modified header")
        return None
    lastmod_date = datetime.strptime(lastmod, '%a, %d %b %Y %H:%M:%S %Z')
    if lastmod_date >= fresh_date:
        return response.content
    else:
        return None
