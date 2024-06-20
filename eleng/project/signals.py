from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver



from .models import Slider, OurServices, Vacancy

@receiver(post_save, sender=Slider)
@receiver(post_delete, sender=Slider)
@receiver(post_save, sender=OurServices)
@receiver(post_delete, sender=OurServices)
@receiver(post_save, sender=Vacancy)
@receiver(post_delete, sender=Vacancy)
def clear_cache(sender, **kwargs):
    """
    Очищает кеш при их изменении или удалении.
    """
    if sender == OurServices:
        cache.delete('ourservices_part1')
        cache.delete('ourservices_part2')
    if sender == Vacancy:
        cache.delete('vacancies')
    if sender == Slider:
        cache.delete('slide')