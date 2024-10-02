import re

from django import template

register = template.Library()


@register.filter
def highlight(full_text, search_term):
    """Wraps all values of search_term"""
    if full_text is None or len(search_term) == 0:
        return full_text

    # Use a replacer function in order to maintain the original case
    def replacer(match):
        return '<span class="u-highlight">{}</span>'.format(match.group(0))

    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    return pattern.sub(replacer, full_text)
