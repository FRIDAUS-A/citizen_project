from django.shortcuts import render
from press.models import Press, PressPost
from press.serializers import PressSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from press.serializers import LoginSerializer, RegistrationSerializer, PressPostSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
import uuid
    
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
            return Response({"message": "Oya Login Press", "csrf_token": csrf_token})
    

class RegisterView(APIView):
    """
    API view for user registration.
    """
    permission_classes = (permissions.AllowAny, )
    def post(self, request, *args, **kwargs):
        data=request.data
        data['groups'] = [1]
        data['user_permissions'] = [28]
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
            csrf_token = get_token(self.request)
            return Response({"message": "Oya Register Press", "csrf_token": csrf_token})

  
class PressDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        press = self.request.user
        serializer = PressSerializer(press)
        return Response(serializer.data)
    def put(self, request, *args, **kwargs):
        press = self.request.user
        obj = Press.objects.get(press_id=press.press_id)
        objDict = obj.__dict__
        objDict.pop('_state')
        data = request.data
        for key, value in data.items():
             objDict[key] = value
        serializer = PressSerializer(press, data=objDict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        press = self.request.user
        press.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PressPostList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        press = self.request.user
        posts = PressPost.objects.filter(press_id=press.press_id)
        serializer = PressPostSerializer(posts, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        press = self.request.user
        data = request.data
        data['press_id'] = press.press_id
        serializer = PressPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PressPostDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    def get_object(self, pk):
        try:
            return PressPost.objects.get(pk=pk)
        except PressPost.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        press = self.request.user
        post = self.get_object(pk)
        if post.press_id == press.pres_id:
            serializer = PressPostSerializer(post)
            return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        press = self.request.user
        post = self.get_object(pk=pk)
        data = request.data
        data['press_id'] = press.press_id
        if 'content' not in data:
            data['content'] = post.content
        serializer = PressPostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)