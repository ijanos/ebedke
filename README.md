# Ebédke

> There are two hard things in computer science, cache invalidation and deciding
> where to eat.

This is stateless Flask app that crawls pages of restaurants and return their
daily menu in JSON format. A small HTML5/JS page is included in the `static`
folder that displays the response in a list.

**Cache the response for an appropriate time to avoid stressing the crawled
servers**

## Development

Use flask to run the development server

```
export FLASK_APP=run.py
flask run
```

A [Facebook app
token](https://developers.facebook.com/docs/facebook-login/access-tokens#apptokens)
is required to read posts from facebook pages.

To test individual  providers invoke them as a separate script. For providers
that use settings from the config use `python -m config provider/provider.py` to
run.

## License


Licensed under either of
  - Apache License, Version 2.0, (LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0)
  - MIT license (LICENSE-MIT or http://opensource.org/licenses/MIT)

at your option.
