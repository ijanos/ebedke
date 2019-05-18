import redis
from ebedke import settings

redis = redis.StrictRedis(host=settings.redis_host,
                          port=settings.redis_port,
                          decode_responses=False)
