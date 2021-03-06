# Development notes

This is a diary-like file to keep notes, ideas and record things that I liked
or surprised me. There is no guarantee I will ever add anything again to this
file.

## 2020-05-27

Upgrading Fedora on the server upgraded python from 3.7 to 3.8. I run 3.8 on my
laptop already and I knew it was working just fine. I had to redeploy the
virtual env so it links to the new python. I did quick smoke test after the
upgrade, everything looked OK. I also have monitoring set up that checks if the
server responds 200 on HTTP. At this point I was pretty sure the upgrade went
fine. Except I have this line in the deploy script:

```
STATIC_DIR={{active_env}}/lib/python3.7/site-packages/ebedke/static
ln -fsn $STATIC_DIR {{static_files}}
```

I symlink the static files directory from the virtual env to a fixed location
where nginx is pointed. Smoketest was most likely fine because of the browser
cache. After the caches expired static assets were all 404. By sheer luck I
noticed the issue pretty early next day so the downtime wasn't too bad.

I did know that `ln` creates symlinks to non-existent things but I didn't think
it was an issue until now. I added a test to the script.

```
test -d $STATIC_DIR
```

The bash script has `set -eux` so it will stop if this test fails. Maybe I
should expand the monitoring as well to keep an eye on the static assets of the
site in future. The deploy script cannot roll back by itself, that would also
be a nice feature.


## 2019-11-16

Two months ago facebook decided to close down its API that allowed access to
public page posts. The API still exist but it requires a business contract and
passing a review process. I tried the review process and as expected the
project did not pass. Other than that, I have no interest, time or money to
open a business just for facebook. The info I am scraping is intended as public
information.

Obvious next step should be start crawling facebook pages but that sounds
painful and really unreliable so I'd rather not go down that road. So what
other options do I have. I figured I can embed facebook pages using the
facebook page plugin. That way the users can see the the posts right on the
page, no need to navigate away.

The page plugin is huge, loading all page plugins slowed down the page
significantly and ate up tens of megabytes of traffic data. I was always proud
of the ebed.today loading fast and using as little data as possible, I am not
going to throw that away for facebook so I enabled on-demand loading of the
plugins.

The whole thing works surprisingly good in practice with one huge caveat. The
facebook based data is missing from the JSON API. Not if I can ever solve this
one.

## 2019-08-18

Figuring out my own way of loading plugins was fun, but my implementation was
brittle. Loading from relative path had the disadvantage of loading only worked
when invoked from the project root directory. By making `plugin_dir` an
argument I thought it will be easier to test loading mocked plugins.

```python
def load_plugins(plugin_dir="ebedke/plugins"):
```

The actual module loading was done through `import_module` which expected a dot
separated module name, so I had to cut the `.py` characters of the extension.

```python
module = importlib.import_module(f"ebedke.plugins.{entry.name[:-3]}")
```

This also killed my hopes of easy testing plugins because the tested code
should also have to know it is currently under test and behave differently.

Turns out the python documentation already has pretty good [tips for
dynamically loading
plugins](https://packaging.python.org/guides/creating-and-discovering-plugins/)
and the standar library has tools for figuring out what modules live in a
package directory. Using `pkguitl` module to load a plugin does not depend on a
specific working directory and no need to juggle the file extensions.


Testing this methos still problematic, it think I will have to monkey around
the `__path__` member of the package but I will solve this another day.

