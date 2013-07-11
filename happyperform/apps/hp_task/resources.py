from tastypie_mongoengine import resources
from .models import Task


class TaskResource(resources.MongoEngineResource):

    class Meta:
        queryset = Task.objects.all()
        # allowed_methods = ('get', 'post')
        resource_name = "task"
