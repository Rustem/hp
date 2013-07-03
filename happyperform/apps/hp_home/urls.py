from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'hp_home.views.index', name='home'),
)
