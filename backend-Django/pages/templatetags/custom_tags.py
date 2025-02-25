from django import template

register = template.Library()

@register.simple_tag
def empty_stars(count):
    return range(count)
