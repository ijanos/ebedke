import os
from importlib import reload
from ebedke import settings

def test_envvar_settings():
    os.environ["FACEBOOK_ACCESS_TOKEN"] = "fbtoken"
    os.environ["GOOGLE_API_KEY"] = "gcptoken"
    reload(settings)
    assert settings.facebook_token == "fbtoken"
    assert settings.google_token == "gcptoken"
    assert settings.debug_mode
