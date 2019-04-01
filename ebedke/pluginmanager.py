import os
import sys
import importlib
from collections import defaultdict
from collections.abc import Iterable
from datetime import timedelta, datetime

from ebedke.utils.text import normalize_menu


class EbedkePlugin(object):
    def __init__(self, *, id, enabled, name, groups, downloader, ttl, url, cards):
        self.id = id
        self.enabled = enabled
        self.name = name
        self.groups = groups
        self.downloader = downloader
        self.ttl = ttl
        self.url = url
        self.cards = cards
        self.check_inputs()

        # ugly hack... but it works, depends on cpython interals
        # it will only run if the caller is __main__
        if sys._getframe(1).f_globals["__name__"] == "__main__":
            self.run()

    def run(self):
        date_offstet = int(sys.argv[1]) if len(sys.argv) >= 2 else 0
        date_offstet = timedelta(days=date_offstet)
        run_date = datetime.today() + date_offstet
        menu = list(self.downloader(run_date))
        assert isinstance(menu, Iterable) and not isinstance(menu, (str, bytes)),\
            "Download function must return a list or other iterable that is not a string or bytestring"
        print("Date:", run_date.strftime("%Y-%m-%d, %A"))
        print("Raw menu:")
        print(menu)
        print("\nNormalized menu:")
        print(normalize_menu(menu))

    def check_inputs(self):
        valid_groups = ["szell", "corvin", "moricz", "ferenciek", "szepvolgyi"]
        valid_cards = ["szep", "erzs"]
        assert isinstance(self.name, str), "Plugin name must be a string"
        assert isinstance(self.id, str), "Plugin ID should be a short string"
        assert len(self.id) > 1, "Plugin ID must be at least 2 characters"
        assert isinstance(self.enabled, bool)
        assert isinstance(self.groups, list)
        assert all(g in valid_groups for g in self.groups)
        assert self.groups, "Groups must not be empty"
        assert callable(self.downloader), "Download must be a function"
        assert isinstance(self.ttl, timedelta), "TTL must be a Timedelta"
        assert self.ttl >= timedelta(minutes=5), "TTL must be larger than 5 minutes"
        assert self.ttl <= timedelta(hours=24), "Larger TTLs are pointless"
        assert isinstance(self.url, str)
        assert self.url.startswith("http")
        assert isinstance(self.cards, list)
        assert all(c in valid_cards for c in self.cards)

    def __repr__(self):
        return f"EbedkePlugin «{self.name}»"

def load_plugins():
    groups = defaultdict(list)
    all = []
    ids = set()
    with os.scandir("ebedke/plugins") as direntries:
        for entry in direntries:
            if entry.name.endswith('.py') and not entry.name.startswith("__") and entry.is_file():
                module = importlib.import_module(f"ebedke.plugins.{entry.name[:-3]}")
                if module.plugin.id in ids:
                    raise Exception(f"Duplicate ids! {module.plugin.name}: {module.plugin.id}")
                ids.add(module.plugin.id)
                if module.plugin.enabled:
                    all.append(module.plugin)
                    for group in module.plugin.groups:
                        groups[group].append(module.plugin)
    groups["all"] = all
    for pluginlist in groups.values():
        pluginlist.sort(key=lambda plugin: plugin.name)
    return groups


if __name__ == "__main__":
    groups = load_plugins()
    for group in groups:
        print(group, groups[group], "\n")
