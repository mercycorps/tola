from django import template
from django.template import Variable, VariableDoesNotExist

register = template.Library()

@register.filter(name='get')
def get(d, k):
    """
    Retrieves an item in dictionary based on its key 
    """
    return d.get(k, None)

@register.filter
def get_by_index(l, i):
    return l[i]

