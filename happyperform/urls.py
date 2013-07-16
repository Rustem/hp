from django.conf.urls import patterns, include, url
from tastypie.api import Api
from hp_task.resources import TaskResource
from hp_user.resources import AuthResource, UserResource
from hp_space.resources import SpaceResource
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(AuthResource())
v1_api.register(UserResource())
v1_api.register(SpaceResource())
# Api resources are accessible by /api/v1/:RESOURCE_NAME
urlpatterns = patterns(
    '',
    url(r'^', include('hp_home.urls')),
    url(r'^api/', include(v1_api.urls)),
    # Examples:
    # url(r'^$', 'happyperform.views.home', name='home'),
    # url(r'^happyperform/', include('happyperform.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
