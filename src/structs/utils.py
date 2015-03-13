from functools import wraps


def memoize(f):
    cache = {}

    @wraps(f)
    def memoized(*args):
        if args in cache:
            return cache[args]
        else:
            result = f(*args)
            cache[args] = result
            return result

    return memoized
