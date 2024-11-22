from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from management.wrappers.safe_execute import safe_execute

__all__ = ['CaseInsensitiveModelBackend']

User = get_user_model()


class CaseInsensitiveModelBackend(ModelBackend):
    @safe_execute()
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')
        try:
            user = User._default_manager.get(username__iexact=username)
        except User.DoesNotExist:
            return User().set_password(password)
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
