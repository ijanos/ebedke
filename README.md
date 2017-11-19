# Ebédke

> There are two hard things in computer science, cache invalidation and deciding
> where to eat.

Ebédke is a stateless Flask app that crawls pages of restaurants and return
their daily menu in JSON format. A small HTML5/JS page is included in the
`static` folder that displays the response as a nice list.

**Cache the response for an appropriate time to avoid stressing the crawled
servers**

## Development

[Pipenv](https://docs.pipenv.org) is the recommended tool to manage dependencies.

First install the dependencies, `--dev` is optional.

```
pipenv install --dev
```

Copy `config.py.example` as `config.py` then use flask to run the development
server:

```
export FLASK_APP=run.py
pipenv run flask run
```

A [Facebook app
token](https://developers.facebook.com/docs/facebook-login/access-tokens#apptokens)
is required to read posts from facebook pages, add yours in `config.py`.

To test individual  providers invoke them as a separate script. For providers
that use settings from the config use `pipenv run python -m provider.name` command structure.


## License


The source code in the repository is licensed under either of
  - Apache License, Version 2.0, (LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0)
  - MIT license (LICENSE-MIT or http://opensource.org/licenses/MIT)

at your option.

The page background pattern is freely available at [Heropatterns](http://www.heropatterns.com/),
licensed under [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/).