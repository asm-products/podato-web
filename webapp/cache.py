"""Small wrapper around App Engine's memcache module, so we can easily swap it out if we move."""
from google.appengine.api import memcache

def set(key, value, expires=0):
    """Stores the given key-value pair, making it expire after 'expires' seconds."""
    return memcache.set(key, value, expires)

def set_multi(pairs, expires=0, key_prefix=""):
    """Sets multiple keys at once. key_prefix is added to every key."""
    return memcache.set(pairs, expires, key_prefix)

def get(key):
    """Get the value associated with the given key."""
    return memcache.get(key)

def get_multi(keys, key_prefix=""):
    """Returns all values associated with the given keys.
    Returns a dictionary mapping keys to values.
    key_prefix is not included in the dictionary keys."""
    return memcache.get(keys, key_prefix)