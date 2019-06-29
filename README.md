# Ebédke 🍽

> There are two hard things in computer science, cache invalidation and deciding
> where to eat.

Ebédke is a Python web crawler that collects the daily menu from
restaurants' webpages. The collected menus are cached in redis and can be viewed in
an HTML page or in JSON format with the included Flask app.

## Architecture

The `updater.py` is a standalone script that will run a loop and update expired
pages every 30 seconds and then pushes them to redis. The `web.py` script is a
simple Flask app that lists daily menus read from redis.

## Development

The python packages dependencies can be found in `pyproject.toml` and can be
managed with [Poetry](https://poetry.eustace.io/).

Use this command to install the dependencies:

```bash
poetry install
```

A [Facebook app
token](https://developers.facebook.com/docs/facebook-login/access-tokens#apptokens)
is required to read posts from facebook pages.
A Google Cloud Vision API key is required for OCR capabilities.

API keys are stored in environment variables.

```bash
export EBEDKE_REDIS_HOST=localhost
export EBEDKE_REDIS_PORT=6379
export FACEBOOK_ACCESS_TOKEN=token
export GOOGLE_API_KEY=apikey
```

Redis is required, please start `redis-server` before running ebekde, running
without redis is not supported.

Running individual plugins is possible as standalone modules like this:

```bash
poetry run python -m ebedke.plugins.pqs
```

An additional arugment can be used to go back or forward in time:

```bash
poetry run python -m ebedke.plugins.pqs -3
```

The Flask dev server is enough for testing purposes but not recommended for
production:

```bash
poetry run python -m ebedke.web
```

Subdomains can be easily be tested with the `xip.io` service.
```
http://test.127.0.0.1.xip.io:5000/
```

## Tests

Some tests are provided in the `tests` directory, they can be run with pytest.

`poetry run pytest`

Type hints are also provided in many places, the project can be type-checked
with mypy checker.

`poetry run mypy -p ebedke`

I also recommend using the pylint python linter with my configuration file

`poetry run pylint --rcfile=pylintrc ebedke`

## Plugins

Plugins live in `ebedke/plugins` as single python files. To add a new plugin
just drop a new file there following this plugin skeleton

```python
from datetime import timedelta
from ebedke.pluginmanager import EbedkePlugin

def download_menu(today):
    return ["menu line 1", "menu line 2"]

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"], # which subdomains it should show up
    name='My Restaurant',
    id='mrr', # a short id string
    url="http://myrestarunt.myrestaruant",
    downloader=download_menu,
    ttl=timedelta(hours=6), # how often should ebedke update the menu
    cards=['szep'] # accepted cafeteria cards
    coord=(47.4, 19.1) # GPS coordinates of the place
)
```

## Deployment

Using a production webserver with a wsgi server like gunicorn or uwsgi is
recommended. An example nginx config is included in the resources directory.

Example gunicron command line

```
gunicorn --bind=0.0.0.0:80 -w 4 ebedke.web:app
```

An ansible playbook is available in the `resources` directroy that deploys a
`ebedke` on Fedora linux.

## License

The source code in the repository is licensed under either of
  - Apache License, Version 2.0, (LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0)
  - MIT license (LICENSE-MIT or http://opensource.org/licenses/MIT)

at your option.