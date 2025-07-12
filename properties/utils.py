from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, timeout=3600)  # 1 hour
    return properties



logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        conn = get_redis_connection("default")
        info = conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = round((hits / total_requests) * 100, 2) if total_requests > 0 else 0.0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }

        logger.info(f"Redis Cache Metrics: Hits={hits}, Misses={misses}, Hit Ratio={hit_ratio}%")
        return metrics

    except Exception as e:
        logger.error(f"Failed to retrieve Redis cache metrics: {str(e)}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0.0,
            "error": str(e),
        }
