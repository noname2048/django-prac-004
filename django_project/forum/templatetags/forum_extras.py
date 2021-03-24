from django import template
import datetime
from dateutil.parser import parse

register = template.Library()


@register.filter(name="time_meter")
def time_meter(value):

    kst = datetime.timezone(datetime.timedelta(hours=9))

    if datetime.datetime.now().replace(tzinfo=kst) - value <= datetime.timedelta(days=20):
        return "green"
    else:
        return "red"
