from functools import wraps

from main import getDailyMenu_parallel

from flask import Flask, send_from_directory, jsonify, request
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

app = Flask(__name__)

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

@app.route('/favicon.png')
def favicon():
    return app.send_static_file('favicon.png')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/menu')
@cached(timeout=15 * 60)
def dailymenu():
    return jsonify(getDailyMenu_parallel())
