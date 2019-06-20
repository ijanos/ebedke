import redis as pyredis
from ebedke import settings

redis = pyredis.StrictRedis(host=settings.redis_host,
                          port=settings.redis_port,
                          decode_responses=False)
