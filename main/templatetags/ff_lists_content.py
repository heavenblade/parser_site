from django import template

register = template.Library()

@register.simple_tag
def get_joined_elements(my_list):
    return(', '.join(my_list))

@register.simple_tag
def get_joined_table_entries(entry):
    if (isinstance(entry, int)):
        return(entry)
    else:
        return(' / '.join(entry))

@register.simple_tag
def check_entry_type(entry):
    if (isinstance(entry, int)):
        return True
    else:
        return False
