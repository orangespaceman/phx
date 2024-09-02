from django import template

register = template.Library()


@register.filter
def highlight(full_text, search_term):
    """Wraps all values of search_term"""
    if full_text is None or len(search_term) == 0:
        return full_text
    replacement_text = '{}{}{}'.format('<span class="u-highlight">',
                                       search_term, '</span>')
    return full_text.replace(search_term, replacement_text)
