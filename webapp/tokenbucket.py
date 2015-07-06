import cache
import datetime
import math

class OutOfTokensException(Exception):
    pass


BUCKET_CACHE_KEY_PREFIX = "TOKEN_BUCKET"

class TokenBucket(object):

    def __init__(self, name, number, per_seconds, bucket_size):
        self.name = name
        self.number = number
        self.per_seconds = per_seconds
        self.bucket_size = bucket_size

    def use(self, amount):
        tokens, last_accessed = self._get_bucket_info()&
        now = int(datetime.datetime.now().strftime("%s"))
        seconds_since = now - last_accessed
        tokens = min(tokens + math.floor((seconds_since/self.per_seconds)*self.number), self.bucket_size)

        if tokens < amount:
            raise OutOfTokensException("You don't have enough tokens left.")
        tokens -= amount

        self._set_bucket_info(tokens, last_accessed)

    def _get_bucket_info(self):
        tokens, last_accessed = (cache.get(BUCKET_CACHE_KEY_PREFIX + self.name) or "0|0").split("|")
        last_accessed = int(last_accessed)
        tokens = int(tokens)
        return tokens, last_accessed

    def _set_bucket_info(self, tokens, last_accessed):
        return cache.set(BUCKET_CACHE_KEY_PREFIX + self.name, "%s|%s" % (tokens, now))