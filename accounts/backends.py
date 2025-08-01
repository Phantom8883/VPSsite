# accounts/backends.py

from django.contrib.auth.backends import ModelBackend
from .models import TLUser

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email_or_phone')
        if username is None or password is None:
            return None

        user = None
        if '@' in username:
            try:
                user = TLUser.objects.get(email=username)
            except TLUser.DoesNotExist:
                return None
        else:
            try:
                user = TLUser.objects.get(tel=username)
            except TLUser.DoesNotExist:
                return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
