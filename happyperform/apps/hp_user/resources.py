from hp_user.models import User
from tastypie_mongoengine import resources
from django.conf.urls import url
from hp_extensions.ex_tastypie import HPAuthentication, ApiKeyAuthentication
import simplejson as json


class HPResponse(object):

    def __init__(self):
        self.is_success = True
        self.retval = {}

    def __call__(self):
        assert isinstance(self.is_success, bool), "Incorrect Response param"
        assert isinstance(self.retval, (list, dict)), "Incorrect Response param"
        return {
            "is_success": self.is_success,
            "retval": self.retval
        }


class AuthResource(resources.MongoEngineResource):

    class Meta:
        resource_name = "auth"
        authentication = HPAuthentication()

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/register/$" % (self._meta.resource_name,),
                self.wrap_view('auth_register'), name="api_register"
            ),
        ]

    def auth_register(self, request, **kwargs):
        self.method_check(request, allowed=["post"])
        self.is_authenticated(request)
        response, params = HPResponse(), json.loads(request.body)
        try:
            user = User.create_user(params["password"], params["email"],)
        except KeyError:
            response.is_success = False
            response.retval = {"reason": "Params[%s] must be specified" % ("email, password")}
            return self.create_response(request, response())
        response.is_success = True
        response.retval = {
            "email": user.pk,
            "password": user.password,
            "api_key": user.api_key
        }
        return self.create_response(request, response())

    def hydrate(self, bundle):
        print bundle.data
        raise


class UserResource(resources.MongoEngineResource):

    class Meta:
        queryset = User.objects.all().order_by('-id')
        allowed_methods = ('get', 'post', 'put', 'delete')
        exclude = ("password", "api_key", "is_active")
        detail_uri_name = "email"
        # authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/(?P<%s>[\w\d._+-]+@[\w\d.-]+\.[A-Za-z]{2,4})/$" % (self._meta.resource_name, self._meta.detail_uri_name),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"
            ),
        ]
