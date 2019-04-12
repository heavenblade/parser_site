from django import template

register = template.Library()

@register.simple_tag
def get_joined_elements(my_list):
    return(', '.join(my_list))
