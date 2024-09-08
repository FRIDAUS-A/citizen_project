from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from citizen.models import Citizen
from press.models import Press

class EmailBackend(ModelBackend):
    print("authenticate citizen and press")
    def authenticate(self, request, username=None, password=None, **kwargs):
        #UserModel = get_user_model()
        try:
            print("Citizen")
            user = Citizen.objects.get(email=username)
            if user.check_password(password):
                return user
        except Citizen.DoesNotExist:
            pass
        try:
            user = Press.objects.get(email=username)
            if user.check_password(password):
                return user
        except Press.DoesNotExist:
            pass

        return None
            