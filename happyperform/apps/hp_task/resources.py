from tastypie_mongoengine import resources
from .models import Task
from hp_extensions.ex_tastypie import ApiKeyAuthentication


class TaskResource(resources.MongoEngineResource):

    class Meta:
        queryset = Task.objects.all()
        resource_name = "ball"
        authentication = ApiKeyAuthentication()
        allowed_methods = ("get", "post", "delete", "put")
        default_format = "application/json"
        excludes = ["_id", "irad", "cur_rad", "miss_days"]
