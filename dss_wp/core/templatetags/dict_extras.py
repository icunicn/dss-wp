from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key."""
    if dictionary is None or not isinstance(dictionary, dict):
        return 0
    try:
        value = dictionary.get(key)
        return value if value is not None else 0
    except (AttributeError, TypeError, KeyError):
        return 0

@register.filter
def div(value, arg):
    """Divide value by arg."""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0
