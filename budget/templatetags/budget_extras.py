#!/usr/bin/env python

from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def dollars(text):
    if not text:
        return text
    if text[0] == '-':
        return '-$' + text[1:]
    else:
        return '$' + text

# vim: et sw=4 sts=4
