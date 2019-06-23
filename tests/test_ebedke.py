from datetime import datetime
import json
from ebedke import pluginmanager
from ebedke import updater
from tests.mock import redis as mocked_redis
from tests.mock import plugins as mock_plugins

def test_all_plugins_loadable():
    pluginmanager.load_plugins()

def test_no_duplicate_ids():
    plugins = pluginmanager.load_plugins()
    ids = []
    for plugin in plugins["all"]:
        ids.append(plugin.id)
    assert len(ids) == len(set(ids))

def test_updater():
    mocked_redis.reset()
    updater.redis = mocked_redis
    test_datetime = datetime(2010, 1, 1, 11, 11)
    updater.update(mock_plugins.test_plugin1, test_datetime)
    expected_json_string = '{"menu": ["test menu line 1", "test menu line 2"], "timestamp": "2010-01-01 11:11:00.000000"}'
    assert mocked_redis.get("test1:menu") == expected_json_string

def test_menus_cleared_at_midnight():
    """
    This test depends on the mocked plugins behavior that they return an emtpy
    menu before 8:00
    """
    mocked_redis.reset()
    updater.redis = mocked_redis
    updater.cache = mocked_redis
    before_midnight_dt = datetime(2019, 6, 24, 11, 11)
    updater.update_restaurants([mock_plugins.test_plugin1, mock_plugins.test_plugin2], before_midnight_dt)
    menu1 = json.loads(mocked_redis.get("test1:menu"))
    menu2 = json.loads(mocked_redis.get("test2:menu"))
    test_menu = mock_plugins.test_menu_list
    assert menu1["menu"] == test_menu and menu2["menu"] == test_menu

    after_midnight_dt = datetime(2019, 6, 25, 0, 5)
    updater.update_restaurants([mock_plugins.test_plugin1, mock_plugins.test_plugin2], after_midnight_dt)
    menu1 = json.loads(mocked_redis.get("test1:menu"))
    menu2 = json.loads(mocked_redis.get("test2:menu"))
    assert menu1["menu"] == [] and menu2["menu"] == []
