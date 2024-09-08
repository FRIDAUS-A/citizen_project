from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from citizen.models import Citizen
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError


User = get_user_model()

"""
class EmailBackend(ModelBackend):
    print("authenticate citizens")
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = Citizen.objects.get(email=username)
        if user.check_password(password):
            return user
        return None
"""


class JWTAuthentication(authentication.BasicAuthentication):

    @classmethod
    def create_jwt(cls, user):
        # Create the JWT payload
        payload = {
            'citizen_id': user.citizen_id,
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS'])).timestamp()),
            # set the expiration time for 5 hour from now
            'iat': datetime.now().timestamp()
        }


        # Encode the JWT with secret key
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token


    def authenticate(self, request):
        # Extract the JWT from the Authorization header

        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None
        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token) # clean the token
    # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.PyJWTError:
            raise AuthenticationFailed('Token is invalid')
        except:
            raise ParseError()


        citizen_id = payload.get('citizen_id')
        if citizen_id is None:
            raise AuthenticationFailed('user is not authorized')

        user = User.objects.filter(citizen_id=citizen_id).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        #print(citizen_id)

    # return the user and token payload
        return user, citizen_id


    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '') # clean token
        return token
    
