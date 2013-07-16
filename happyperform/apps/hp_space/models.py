import mongoengine as me
from django.utils.translation import ugettext_lazy as _


class Space(me.Document):

    sid = me.SequenceField(
        required=True,
        verbose_name=_("unique auto-inc id"),
        primary_key=True)

    title = me.StringField(
        required=True,
        verbose_name=_("space title"))

    color = me.IntField(
        required=False,
        verbose_name=_("space color"),
        default=0)

    balls = me.ListField(
        me.ReferenceField("Task", dbref=True),
        verbose_name=_("space balls"),
        default=[])
