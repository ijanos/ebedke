import sys
import importlib
import pkgutil
from typing import List, Dict, Callable, Tuple, Union
from collections import defaultdict
from datetime import timedelta, datetime

import ebedke.plugins
from ebedke.utils.text import normalize_menu

# Type aliases
Coordinates = Union[Tuple[float, float], List[Tuple[float, float]]]
Downloader = Callable[[datetime], List[str]]

class EbedkePlugin:
    # pylint: disable=redefined-builtin,protected-access,too-many-instance-attributes
    def __init__(self, *, id: str, enabled: bool, name: str, groups: List[str],
                 downloader: Downloader, ttl: timedelta, url: str, cards: List[str], coord: Coordinates) -> None:
        self.id = id
        self.enabled = enabled
        self.name = name
        self.groups = groups
        self.downloader = downloader
        self.ttl = ttl
        self.url = url
        self.cards = cards
        self.coord = coord
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
        assert not isinstance(menu, (str, bytes)), "must return a list not a string" # type: ignore
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
        assert all(g in valid_groups for g in self.groups), "must use pre-defined groups"
        assert self.groups, "Groups must not be empty"
        assert callable(self.downloader), "Download must be a function"
        assert isinstance(self.ttl, timedelta), "TTL must be a Timedelta"
        assert self.ttl >= timedelta(minutes=5), "TTL must be larger than 5 minutes"
        assert self.ttl <= timedelta(hours=24), "Larger TTLs are pointless"
        assert isinstance(self.url, str)
        assert self.url.startswith("http")
        assert isinstance(self.cards, list)
        assert all(c in valid_cards for c in self.cards)
        list_of_tuples = all(isinstance(c, tuple) for c in self.coord) and  isinstance(self.coord, list)
        assert  list_of_tuples or isinstance(self.coord, tuple), "Coord is either a tuple of coordinates or a list of tuples"
        coords: List[Tuple[float, float]]
        coords = self.coord if list_of_tuples else [self.coord] # type: ignore

        for lat, long in coords:
            assert 18.7 < long < 19.4, "Place is in Budapest"
            assert 47.3 < lat < 47.6, "Place is in Budapest"

    def __repr__(self) -> str:
        return f"EbedkePlugin «{self.name}»"


def load_plugin(name: str) -> EbedkePlugin:
    module = importlib.import_module(f"ebedke.plugins.{name}")
    plugin: EbedkePlugin = module.plugin  # type: ignore
    return plugin


def load_plugins() -> Dict[str, List[EbedkePlugin]]:
    groups: Dict[str, List[EbedkePlugin]] = defaultdict(list)
    plugin_path = ebedke.plugins.__path__ # type: ignore  # mypy issue #1422
    modules = [name for _, name, is_pkg in pkgutil.iter_modules(plugin_path) if not is_pkg and not name.startswith('_')]
    for name in modules:
        plugin = load_plugin(name)
        if plugin.enabled:
            groups["all"].append(plugin)
            for group in plugin.groups:
                groups[group].append(plugin)
        else:
            print(f"[ebedke] {plugin} is disabled")
    for pluginlist in groups.values():
        pluginlist.sort(key=lambda plugin: plugin.name)
    return groups


def main():
    groups = load_plugins()
    for group in groups:
        print(f"Group {group}:\n", groups[group], "\n")


if __name__ == "__main__":
    main()
