from __future__ import absolute_import

from functools import wraps

USE_LOCAL_CACHE = True


def local_memoize(obj):
    """In-memory caching to return same value when called with the same arguments.
    WARNING: this caching is local to processes so it's perfect for maintaining a single instance of the clients
    (schemaless, heatpipe, caesar, etc). For global caching for saving computation purposes, use Redis caching instead.
    """
    local_cache = obj.cache = {}

    @wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if USE_LOCAL_CACHE:
            if key not in local_cache:
                local_cache[key] = obj(*args, **kwargs)
            return local_cache[key]
        else:
            return obj(*args, **kwargs)
    return memoizer
