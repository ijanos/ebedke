# Development notes

This is a diary-like file to keep notes, ideas and record things that I liked
or surprised me. There is no guarantee I will ever add anything again to this
file.

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

