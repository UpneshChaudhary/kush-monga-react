# pages/templatetags/stars_range.py

from django import template

register = template.Library()

@register.filter
def stars_range(value):
    return range(1, value + 1)
