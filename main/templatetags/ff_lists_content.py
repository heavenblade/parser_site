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

@register.simple_tag
def check_multiply_defined(table):
    mult_def = False
    for idx_row, row in enumerate(table):
        for idx_col in range(len(row)):
            if (idx_col != 0):
                if (len(table[idx_row][idx_col]) > 1):
                    mult_def = True
                    break
    return mult_def
