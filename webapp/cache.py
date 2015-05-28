from flask.ext.redis import Redis

redis = Redis()

def _add_key_prefix(collection, prefix):
    if isinstance(collection, dict):
        return {prefix + key: value for key, value in collection}
    elif isinstance(collection, list):
        return [prefix + key for key in collection]
    else:
        raise ValueError("Expected dictionary or list, got %s" % type(collection))

def init_cache(app):
    redis.init_app(app)

def set(name, value, expires=0):
    """Sets the value for the given key. If expires is not 0, the value will be removed after the given number of seconds."""
    if expires == 0:
        return redis.set(key, value)
    return redis.setex(name, value, expires)

def set_multi(pairs, expires=0, key_prefix=""):
    """Sets multiple keys at once. key_prefix is added to every key."""
    if key_prefix:
        pairs = _add_key_prefix(pairs, key_prefix)
    if expires == 0:
        return redis.mset(pairs)
    p = redis.pipeline()
    p.mset(pairs)
    for name in pairs:
        p.expire(name, expires)
    return p.execute()

def get(key):
    """Get the value associated with the given key."""
    return redis.get(key)

def get_multi(keys, key_prefix=""):
    """Returns all values associated with the given keys.
    Returns a dictionary mapping keys to values.
    key_prefix is not included in the dictionary keys."""
    if key_prefix:
        keys = _add_key_prefix(keys, key_prefix)

    return redis.mget(keys)