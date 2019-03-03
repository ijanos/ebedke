import os
import importlib
from collections import defaultdict


def load_plugins():
    groups = defaultdict(list)
    all = []
    with os.scandir("plugins") as direntries:
        for entry in direntries:
            if entry.name.endswith('.py') and entry.is_file():
                module = importlib.import_module(f"plugins.{entry.name[:-3]}")
                all.append(module.plugin)
                for group in module.plugin.groups:
                    groups[group].append(module.plugin)
    groups["all"] = all
    for pluginlist in groups.values():
        pluginlist.sort(key=lambda plugin: plugin.name)
    return groups

if __name__ == "__main__":
    groups = load_plugins()
    print(groups)