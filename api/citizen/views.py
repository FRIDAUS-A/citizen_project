from django.shortcuts import render

# Create your views here.
from citizen.models import Citizen, Comment
from press.models import PressPost
from citizen.serializers import CitizenSerializer, CommentSerializer
from press.serializers import PressPostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from citizen.serializers import LoginSerializer, RegistrationSerializer
from django.contrib.auth import login
from rest_framework import permissions
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
            return Response({"message": "Oya Login", "csrf_token": csrf_token})
    

class RegisterView(APIView):
    """
    API view for user registration.
    """
    permission_classes = (permissions.AllowAny, )
    def post(self, request, *args, **kwargs):
        data = request.data
        data['groups'] = [2]
        data['user_permissions'] = [28]
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
            csrf_token = get_token(self.request)
            return Response({"message": "Register Baba", "csrf_token": csrf_token})

  
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
        obj = Citizen.objects.get(citizen_id=citizen.citizen_id)
        objDict = obj.__dict__
        objDict.pop('_state')
        data = request.data
        for key, value in data.items():
             objDict[key] = value
        serializer = CitizenSerializer(citizen, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        citizen = self.request.user
        citizen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        citizen = self.request.user
        comments = Comment.objects.filter(citizen_id=citizen.citizen_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        citizen = self.request.user
        data = request.data
        post =  PressPost.objects.get(post_id=data["post_id"])
        data["post_id"] = post.post_id
        data["citizen_id"] = citizen.citizen_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewPostList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        posts = PressPost.objects.all()
        serializer = PressPostSerializer(posts, many=True)
        return Response(serializer.data)


class ViewPostDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    def get_object(self, pk):
        try:
            return PressPost.objects.get(pk=pk)
        except PressPost.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PressPostSerializer(post)
        return Response(serializer.data)