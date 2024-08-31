from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Comment

register = template.Library()


@register.simple_tag
def get_commented_articles(id=None):
    # context = Comment.objects.select_related('post').filter(post_id=6)
    context = Comment.objects.select_related('comments').filter(articles_id=id).count()

    return context
