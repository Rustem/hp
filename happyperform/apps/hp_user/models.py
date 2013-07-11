import mongoengine as me
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password, make_password
import hmac
import re
import uuid
try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.sha


EMAIL_RE = re.compile(r'^[\w\d._%+-]+@[\w\d.-]+\.[A-Za-z]{2,4}$')


class User(me.Document):

    email = me.StringField(
        required=True,
        regex=EMAIL_RE,
        primary_key=True,
        verbose_name=_("email address"))
    is_active = me.BooleanField(default=True, verbose_name=_("active")) 
    password = me.StringField(max_length=128, verbose_name=_('password'))
    api_key = me.StringField(max_length=256, default='')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    meta = {
        'allow_inheritance': False,
    }

    def __unicode__(self):
        return self.pk

    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        """Sets the user's password - always use this rather than directly
        assigning to :attr:`~mongoengine.django.auth.User.password` as the
        password is hashed before storage.
        """
        self.password = make_password(raw_password)
        self.save()
        return self

    def check_password(self, raw_password):
        """Checks the user's password against a provided password - always use
        this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is
        hashed before storage.
        """
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = self.generate_key()
        return super(User, self).save(*args, **kwargs)

    def generate_key(self):
        new_uuid = uuid.uuid4()
        return hmac.new(str(new_uuid), digestmod=sha1).hexdigest()

    @classmethod
    def create_user(cls, password, email):
        """Create (and save) a new user with the given username, password and
        email address.
        """
        user = cls(email=email)
        user.set_password(password)
        user.save()
        return user
