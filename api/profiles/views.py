from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from citizen.models import Citizen
from citizen.serializers import CitizenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class ProfileDetail(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="get the user profile",
        responses={200: CitizenSerializer}
    )
    def get(self, request):
        #auth_instance = JWTAuthentication()
        #user = auth_instance.authenticate(request)
        user = self.request.user
        serializer = CitizenSerializer(user)
        return Response(serializer.data)


    @swagger_auto_schema(
        operation_description="update your comment",
        request_body=CitizenSerializer, 
        responses={201: CitizenSerializer, 400: 'Bad Request'}
    )
    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = CitizenSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="delete a user account", 
        responses={204: "user account deleted successfuly"}
    )
    def delete(self, request):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)