from django.contrib.auth.backends import ModelBackend
from .models import Users

class EmailOrMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            if '@' in username:
                user = Users.objects.get(email=username)
            else:
                user = Users.objects.get(mobile_no=username)
        except Users.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
