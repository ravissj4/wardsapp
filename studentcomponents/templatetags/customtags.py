from django.template import Library

register = Library()


@register.simple_tag
def define(the_string):
    return sum(d.get('j.fees_paid') for d in the_string)


@register.filter
def running_total(js_paid):
    return sum(d.get('fees_paid') for d in js_paid)


