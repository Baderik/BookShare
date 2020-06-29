from django.contrib.auth.backends import ModelBackend

from authentication.models import User


class MyLoginBackend(ModelBackend):
    def authenticate(self, username=None, email=None, password=None, *args, **kwargs):
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None
