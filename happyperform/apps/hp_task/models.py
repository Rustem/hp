import mongoengine as me
from django.utils.translation import ugettext_lazy as _


class BallMixin(object):
    pass


class Task(BallMixin, me.Document):
    descr = me.StringField(required=True, verbose_name=_("description"))
    dc = me.StringField(required=True, verbose_name=_("date created"))
