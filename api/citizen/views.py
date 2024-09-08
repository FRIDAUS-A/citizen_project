from django.shortcuts import render

# Create your views here.
from citizen.models import Citizen
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from citizen.serializers import LoginSerializer, RegistrationSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
import uuid
from citizen.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
    
class LoginView(APIView):
    """
    API view for user login using email and password.
    """
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="Login with your email and password",
        request_body=LoginSerializer, 
        responses={200: LoginSerializer, 400: 'Bad Request'}
    )
    #@method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = JWTAuthentication.create_jwt(user)
        # Log in the user
        # Example: if using Django's login function

        return Response({"message": "Login successful"}, status=status.HTTP_200_OK, headers={"Authorization": token})
        
    

class RegisterView(APIView):
    """
    API view for user registration.
    """
    permission_classes = (AllowAny, )
    @swagger_auto_schema(
        operation_description="Register as a citizen or press",
        request_body=RegistrationSerializer, 
        responses={201: RegistrationSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        data["citizen_id"] = str(uuid.uuid4())
        #data['groups'] = [2]
        #data['user_permissions'] = [28]
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
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
"""