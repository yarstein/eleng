from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver

from .models import News


@receiver(post_save, sender=News)
@receiver(post_delete, sender=News)
def clear_cache(sender, **kwargs):
    """
    Очищает кеш при их изменении или удалении.
    """
    cache.delete('news_list')
