from django import template
import datetime
from dateutil.parser import parse
from forum.models import ForumComment
from accounts.models import User

register = template.Library()


@register.filter(name="time_meter")
def time_meter(value):

    kst = datetime.timezone(datetime.timedelta(hours=9))

    if datetime.datetime.now().replace(tzinfo=kst) - value <= datetime.timedelta(days=20):
        return "green"
    else:
        return "red"


@register.filter(name="is_user_like")
def is_user_like(comment: ForumComment, user):
    return comment.forumlike_set.filter(author_id=user.id).exists()
