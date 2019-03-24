from ebedke import pluginmanager

def test_all_plugins_loadable():
    pluginmanager.load_plugins()

def test_no_duplicate_ids():
    plugins = pluginmanager.load_plugins()
    ids = []
    for plugin in plugins["all"]:
        ids.append(plugin.id)
    assert len(ids) == len(set(ids))
