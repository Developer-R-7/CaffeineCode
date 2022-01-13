
from django.core.cache import cache



def cache_manager(key,cachedData,time):
    query = cache.get_or_set(key,cachedData,time)
    return query