from whatever.models import CustomUser
from django.contrib.auth.backends import ModelBackend

class NoAuthBackend(ModelBackend):
    """
    Authenticates against signup.models.CustomUser, without requiring
    authorisation
    """
    def authenticate(self, username=None, password=None):
        try:
            return CustomUser.objects.get(username=username)            
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

