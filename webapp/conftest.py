import pytest
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


@pytest.fixture
def mock_cache(monkeypatch):
    clock = ChangableClock()
    redis = mockredis.MockRedis(clock=clock)
    monkeypatch.setattr(cache, "redis", redis)
    return redis, clock