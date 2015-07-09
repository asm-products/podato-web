import cache
import mockredis
import datetime

class ChangableClock(object):
    def __init__(self, now=None):
        self._now = now or datetime.datetime.now()

    def set_time(self, now):
        self._now = now

    def now(self):
        return self._now


def test_cache_set(monkeypatch):
    redis = mockredis.mock_redis_client()
    monkeypatch.setattr(cache, "redis", redis)
    cache.set("foo", "bar")
    assert redis.get("foo") == "bar"


def test_cache_get(monkeypatch):
    redis = mockredis.mock_redis_client()
    monkeypatch.setattr(cache, "redis", redis)
    redis.set("foo", "bar")
    assert cache.get("foo") == "bar"


def test_cache_set_expire(monkeypatch):
    clock = ChangableClock()
    redis = mockredis.MockRedis(clock=clock)
    monkeypatch.setattr(cache, "redis", redis)
    cache.set("foo", "bar", expires=60)
    assert cache.get("foo") == "bar"
    clock.set_time(datetime.datetime.now() + datetime.timedelta(seconds=61))
    redis.do_expire()
    assert cache.get("foo") == None


def test_set_multi(monkeypatch):
    redis = mockredis.mock_redis_client()
    monkeypatch.setattr(cache, "redis", redis)
    cache.set_multi({"foo1": "bar1", "foo2": "bar2"})
    assert redis.get("foo1") == "bar1"
    assert redis.get("foo2") == "bar2"


def test_set_multi_prefix(monkeypatch):
    redis = mockredis.mock_redis_client()
    monkeypatch.setattr(cache, "redis", redis)
    cache.set_multi({"foo1": "bar1", "foo2": "bar2"}, key_prefix="test_")
    assert redis.get("test_foo1") == "bar1"
    assert redis.get("test_foo2") == "bar2"
    assert redis.get("foo1") == None


def test_set_multi_expires(monkeypatch):
    clock = ChangableClock()
    redis = mockredis.MockRedis(clock=clock)
    monkeypatch.setattr(cache, "redis", redis)
    cache.set_multi({"foo1": "bar1", "foo2": "bar2"}, expires=60)
    assert redis.get("foo1") == "bar1"
    assert redis.get("foo2") == "bar2"
    clock.set_time(datetime.datetime.now() + datetime.timedelta(seconds=61))
    redis.do_expire()
    assert redis.get("foo1") == None
    assert redis.get("foo2") == None


def test_get_multi(monkeypatch):
    redis = mockredis.mock_redis_client()
    monkeypatch.setattr(cache, "redis", redis)
    redis.set("foo1", "bar1")
    redis.set("foo2", "bar2")
    assert cache.get_multi(["foo1", "foo2"]) == {"foo1": "bar1", "foo2": "bar2"}


def test_get_multi_prefix(monkeypatch):
    redis = mockredis.mock_redis_client()
    monkeypatch.setattr(cache, "redis", redis)
    redis.set("test-foo1", "bar1")
    redis.set("test-foo2", "bar2")
    assert cache.get_multi(["foo1", "foo2"], key_prefix="test-") == {"foo1": "bar1", "foo2": "bar2"}