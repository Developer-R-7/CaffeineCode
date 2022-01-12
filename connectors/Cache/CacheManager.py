
from django.core.cache import cache



def cache_manager(key,cachedData,time):
    # check if cache key exits
    # Then if not cache then create cache
    query = cache.get_or_set(key,cachedData,time)
    return query