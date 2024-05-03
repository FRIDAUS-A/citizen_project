from django.shortcuts import render

# Create your views here.
from citizen.models import Citizen
from citizen.serializers import CitizenSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from citizen.serializers import LoginSerializer, RegistrationSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token

    
class LoginView(APIView):
    """
    API view for user login using email and password.
    """
    permission_classes = (permissions.AllowAny,)
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # Log in the user
        login(request, user)  # Example: if using Django's login function

        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    
    
    def get(self, request):
            csrf_token = get_token(self.request)
            return Response({"message": "Oya Login", "csrf_token": csrf_token})
    

class RegisterView(APIView):
    """
    API view for user registration.
    """
    permission_classes = (permissions.AllowAny, )
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
class CitizenDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        citizen = self.request.user
        serializer = CitizenSerializer(citizen)
        print(serializer.data)
        return Response(serializer.data)
    def put(self, request, *args, **kwargs):
        citizen = self.request.user
        data = request.data
        if 'email' not in data:
            data['email'] = citizen.email
        if 'phone_number' not in data:
            data['phone_number'] = citizen.phone_number
        serializer = CitizenSerializer(citizen, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        citizen = self.request.user
        citizen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)