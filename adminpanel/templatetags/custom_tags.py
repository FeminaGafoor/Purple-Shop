from django import template

register = template.Library()

@register.filter
def changed(value):
    changed.last = getattr(changed, 'last', None)
    if value != changed.last:
        changed.last = value
        return True
    return False