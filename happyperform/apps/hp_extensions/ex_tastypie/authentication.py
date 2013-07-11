from tastypie.authentication import (
    ApiKeyAuthentication as OldApiKeyAuthentication,
    Authentication)

from tastypie.compat import User
from django.conf import settings
import simplejson as json


class HPAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        data = request.META.get("HTTP_AUTHORIZATION", None)
        is_hp = False
        if data:
            auth_type, key = data.split()
            if auth_type != 'hpkey':
                return False
            is_hp = key == settings.HP_KEY
        else:
            try:
                params = json.loads(request.body)
            except:
                return False
            is_hp = settings.HP_KEY == params.get("api_key", None)
            
        return is_hp


class ApiKeyAuthentication(OldApiKeyAuthentication):
    r"""Basic API key auth backend.

    If information in HEADERS, then:
        HTTP_AUTHORIZATION => apikey r.kamun@gmail.com:[APIKEY]
    """
    def extract_credentials(self, request):
        if request.META.get('HTTP_AUTHORIZATION') and request.META['HTTP_AUTHORIZATION'].lower().startswith('apikey '):
            (auth_type, data) = request.META['HTTP_AUTHORIZATION'].split()

            if auth_type.lower() != 'apikey':
                raise ValueError("Incorrect authorization header.")

            email, api_key = data.split(':', 1)
        else:
            email = request.GET.get('email') or request.POST.get('email')
            api_key = request.GET.get('api_key') or request.POST.get('api_key')

        return email, api_key

    def is_authenticated(self, request, **kwargs):
        r"""Finds the user and checks it's by API key."""

        try:
            email, api_key = self.extract_credentials(request)
        except ValueError:
            return self._unauthorized()

        if not email or not api_key:
            return self._unauthorized()

        try:
            user = User.objects.get(pk=email)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return self._unauthorized()

        if user.is_active():
            return False
        return self.get_key(user, api_key)

    def get_key(self, user, api_key):
        if not user.api_key == api_key:
            return self._unauthorized()
        return True
