from functools import wraps

from main import getDailyMenu_parallel

from flask import Flask, jsonify, request
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

app = Flask(__name__, static_url_path='')

def cached(timeout=5 * 60, key='view/%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/menu')
@cached(timeout=15 * 60)
def dailymenu():
    return jsonify(getDailyMenu_parallel())
