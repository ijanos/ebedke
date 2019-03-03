import sys
from datetime import timedelta


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

    def run(self):
        print(">>> run standalone")

    def check_inputs(self):
        valid_groups = ["szell", "corvin", "moricz", "ferenciek", "szepvolgyi"]
        assert isinstance(self.name, str), "Plugin name must be a string"
        assert isinstance(self.id, str), "Plugin ID should be a short string"
        assert isinstance(self.enabled, bool)
        assert isinstance(self.groups, list)
        assert all(g in valid_groups for g in self.groups)
        assert len(self.groups) > 0
        assert callable(self.downloader), "Download must be a function"
        assert isinstance(self.ttl, timedelta), "TTL must be a Timedelta"
        assert isinstance(self.url, str)
        assert self.url.startswith("http")
        # assert cards

    def __repr__(self):
        return f"EbedkePlugin «{self.name}»"
