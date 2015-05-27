"""Small wrapper around App Engine's memcache module, so we can easily swap it out if we move."""

#TODO reimplement using Redis

def set(key, value, expires=0):
    """Stores the given key-value pair, making it expire after 'expires' seconds."""
    raise NotImplemented

def set_multi(pairs, expires=0, key_prefix=""):
    """Sets multiple keys at once. key_prefix is added to every key."""
    raise NotImplemented

def get(key):
    """Get the value associated with the given key."""
    raise NotImplemented

def get_multi(keys, key_prefix=""):
    """Returns all values associated with the given keys.
    Returns a dictionary mapping keys to values.
    key_prefix is not included in the dictionary keys."""
    raise NotImplemented