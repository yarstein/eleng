from django import template
from django.db.models import Count, Q

from catalog.models import TagProduct


register = template.Library()


@register.simple_tag
def popular_tags():
    tags = TagProduct.objects.annotate(num_times=Count('product_tags', filter=Q(product_tags__is_published=True))).order_by('-num_times')
    tag_list = list(tags.values('tag', 'num_times', 'slug'))
    return tag_list