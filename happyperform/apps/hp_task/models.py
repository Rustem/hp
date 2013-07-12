import mongoengine as me
from django.utils.translation import ugettext_lazy as _
import datetime


class BallMixin(object):
    irad = me.FloatField(default=2.0, verbose_name=_("initial radius"))
    cur_rad = me.FloatField(default=2.0, verbose_name=_("current radius"))
    miss_days = me.ListField(
        me.IntField(),
        default=[], verbose_name=_("missed days"))


class Task(BallMixin, me.Document):
    descr = me.StringField(required=True, verbose_name=_("description"))
    cd = me.DateTimeField(required=True, verbose_name=_("date created"))
    dd = me.DateTimeField(required=True, verbose_name=_("deadline date"))
    creator = me.ReferenceField(
        "User",
        dbref=True, required=True, verbose_name=_("creator"))

    def save(self, *args, **kwargs):
        self.cd = datetime.datetime.utcnow()
        super(Task, self).save(*args, **kwargs)
