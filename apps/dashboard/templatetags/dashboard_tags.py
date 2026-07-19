from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Template filter to access dict items by key, e.g. dict|get_item:key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, "")
    return ""
