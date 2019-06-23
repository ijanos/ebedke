import os
import sys
import importlib
from typing import List, Set, Dict, Callable
from collections import defaultdict
from collections.abc import Iterable
from datetime import timedelta, datetime

from ebedke.utils.text import normalize_menu


class EbedkePlugin:
    # pylint: disable=redefined-builtin,protected-access,too-many-instance-attributes
    def __init__(self, *, id: str, enabled: bool, name: str, groups: List[str],
                 downloader: Callable[[datetime], List[str]], ttl: timedelta, url: str, cards: List[str]) -> None:
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

    def run(self) -> None:
        argv1 = int(sys.argv[1]) if len(sys.argv) >= 2 else 0
        date_offstet = timedelta(days=argv1)
        run_date = datetime.today() + date_offstet
        menu = list(self.downloader(run_date))
        assert isinstance(menu, Iterable) and not isinstance(menu, (str, bytes)),\
            "Download function must return a list or other iterable that is not a string or bytestring"
        print("Date:", run_date.strftime("%Y-%m-%d, %A"))
        print("Raw menu:")
        print(menu)
        print("\nNormalized menu:")
        print(normalize_menu(menu))

    def check_inputs(self) -> None:
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

    def __repr__(self) -> str:
        return f"EbedkePlugin «{self.name}»"

def load_plugins(plugin_dir: str = "ebedke/plugins") -> Dict[str, List[EbedkePlugin]]:
    groups: Dict[str, List[EbedkePlugin]] = defaultdict(list)
    ids: Set[str] = set()
    with os.scandir(plugin_dir) as direntries:
        for entry in direntries:
            if entry.name.endswith('.py') and not entry.name.startswith("__") and entry.is_file():
                module = importlib.import_module(f"ebedke.plugins.{entry.name[:-3]}")
                plugin: EbedkePlugin = getattr(module, "plugin")
                assert plugin.id not in ids, "IDs must be unique"
                ids.add(plugin.id)
                if plugin.enabled:
                    groups["all"].append(plugin)
                    for group in plugin.groups:
                        groups[group].append(plugin)
    for pluginlist in groups.values():
        pluginlist.sort(key=lambda plugin: plugin.name)
    return groups


def main():
    groups = load_plugins()
    for group in groups:
        print(group, groups[group], "\n")


if __name__ == "__main__":
    main()
