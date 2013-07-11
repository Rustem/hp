import mongoengine as me
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password, make_password


class User(me.Document):

    email = me.EmailField(verbose_name=_("email address"))
    is_active = me.BooleanField(default=True, verbose_name=_("active")) 
    password = me.StringField(max_length=128, verbose_name=_('password'))

    username = me.StringField(max_length=30, required=True, verbose_name=_("username"))

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    meta = {
        'allow_inheritance': True,
        'indexes': [
            {'fields': ['username'], 'unique': True, 'sparse': True}
        ]
    }

    def __unicode__(self):
        return self.usernames

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

    @classmethod
    def create_user(cls, username, password, email=None):
        """Create (and save) a new user with the given username, password and
        email address.
        """
        now = datetime_now()

        # Normalize the address by lowercasing the domain part of the email
        # address.
        if email is not None:
            try:
                email_name, domain_part = email.strip().split('@', 1)
            except ValueError:
                pass
            else:
                email = '@'.join([email_name, domain_part.lower()])

        user = cls(username=username, email=email, date_joined=now)
        user.set_password(password)
        user.save()
        return user

