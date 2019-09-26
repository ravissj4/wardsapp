from django import template
from django.contrib.auth.models import Group


register = template.Library()


@register.filter(name='staff')
def staff(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='parent')
def parent(user, group_name):
    return user.groups.filter(name=group_name).exists()
