import os
import importlib
from collections import defaultdict


def load_plugins():
    groups = defaultdict(list)
    all = []
    ids = set()
    with os.scandir("plugins") as direntries:
        for entry in direntries:
            if entry.name.endswith('.py') and not entry.name.startswith("__") and entry.is_file():
                module = importlib.import_module(f"plugins.{entry.name[:-3]}")
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
