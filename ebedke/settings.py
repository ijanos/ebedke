import os

redis_host = os.getenv("EBEDKE_REDIS_HOST", "localhost")
redis_port = int(os.getenv("EBEDKE_REDIS_PORT", "6379"))
facebook_token = os.getenv("FACEBOOK_ACCESS_TOKEN", "")
google_token = os.getenv("GOOGLE_API_KEY", "")
debug_mode =  os.getenv("EBEDKE_LIVE") is None
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"