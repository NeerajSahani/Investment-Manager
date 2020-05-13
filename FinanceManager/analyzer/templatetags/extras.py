import datetime

from django import template
from ..chatbot_utilities import correction

register = template.Library()


@register.filter
def correct(value):
    correction(value)


@register.filter
def get_today(data):
    return data[-1][1]


@register.filter
def sub(value, arg):
    return int(value - arg)


@register.filter
def pct(value, arg):
    return round((value - arg) / value * 100, ndigits=4)


@register.filter
def absolute(value):
    return abs(value)


@register.filter
def days_from_today(value):
    out = (value - datetime.date.today()).days
    return out if out > 0 else 'Ended'


@register.filter
def mul(value, arg):
    return value * arg


@register.simple_tag
def result(arg1, arg2, arg3):
    return (arg1 - arg2) * arg3
