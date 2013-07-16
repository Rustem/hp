from tastypie_mongoengine import resources
from .models import Space
# from .forms import SpaceForm
from hp_extensions.ex_tastypie import ApiKeyAuthentication
# from hp_extensions.ex_tastypie import CleanedDataFormValidation
from tastypie.authorization import Authorization
from django.conf.urls import url


class SpaceResource(resources.MongoEngineResource):

    class Meta:
        queryset = Space.objects.all()
        resource_name = "space"
        # authentication = ApiKeyAuthentication()
        authorization = Authorization()
        default_format = "application/json"

    def obj_get(self, bundle, **kwargs):
        kwargs["pk"] = int(kwargs["pk"])
        return super(SpaceResource, self).obj_get(bundle, **kwargs)