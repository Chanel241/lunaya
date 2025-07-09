
from django import template
from ..models import Horoscope

register = template.Library()

@register.filter
def get_sign_display(value):
    for choice in Horoscope._meta.get_field('sign').choices:
     if choice[0] == value:
            return choice[1]
    return value