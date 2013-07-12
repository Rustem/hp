from tastypie_mongoengine import resources
from .models import Task
from .forms import TaskForm
from hp_extensions.ex_tastypie import ApiKeyAuthentication
from hp_extensions.ex_tastypie import CleanedDataFormValidation
from tastypie_mongoengine import fields as tp_fields
from tastypie.authorization import Authorization
from django.core.urlresolvers import reverse


class TaskResource(resources.MongoEngineResource):

    creator = tp_fields.ReferenceField(
        to="hp_user.resources.UserResource",
        attribute="creator", full=True)

    class Meta:
        queryset = Task.objects.all()
        resource_name = "ball"
        # authentication = ApiKeyAuthentication()
        validation = CleanedDataFormValidation(form_class=TaskForm)
        authorization = Authorization()
        allowed_methods = ("get", "post", "delete", "put")
        default_format = "application/json"
        excludes = ["cd", "id", "irad", "cur_rad", "miss_days"]
