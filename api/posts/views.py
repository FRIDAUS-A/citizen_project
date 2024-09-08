from django.shortcuts import render
from posts.models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from posts.serializers import PostSerializer
from rest_framework.exceptions import PermissionDenied 
from django.http import Http404
import uuid
from drf_yasg.utils import swagger_auto_schema

# Create your views 

class PostList(APIView):
	permission_classes = [IsAuthenticated]
	@swagger_auto_schema(
        operation_description="get all posts of the user",
        responses={200: PostSerializer(many=True)}
    )
	def get(self, request, format=None):
		posts = Post.objects.filter(citizen_id=request.user.citizen_id)
		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data)



	@swagger_auto_schema(
        operation_description="create a post, you only need the post field",
        request_body=PostSerializer, 
        responses={201: PostSerializer, 400: 'Bad Request'}
    )
	def post(self, request, format=None):
		permission_classes = [IsAuthenticated]
		user = self.request.user
		if (not user.is_press):
			raise PermissionDenied('User does not have permission to post')
		data = request.data
		data["citizen"] = user.citizen_id
		data["post_id"] = str(uuid.uuid4())
		serializer = PostSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response({"message":"post created successfully","data": serializer.data}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
	permission_classes = [IsAuthenticated]
	def get_object(self, pk):
		user = self.request.user
		if (not user.is_press):
			raise PermissionDenied('User does not have permission to post')
		try:
			return Post.objects.get(pk=pk)
		except Post.DoesNotExist:
			raise Http404
	@swagger_auto_schema(
        operation_description="get a particular post with its id",
        responses={200: PostSerializer}
    )
	def get(self, request, pk, format=None):
		post = self.get_object(pk)
		serializer = PostSerializer(post)
		return Response(serializer.data)


	@swagger_auto_schema(
        operation_description="update your post",
        request_body=PostSerializer, 
        responses={201: PostSerializer, 400: 'Bad Request'}
    )
	def put(self, request, pk, format=None):
		post = self.get_object(pk)
		serializer = PostSerializer(post, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	@swagger_auto_schema(
        operation_description="delete a post using its id", 
        responses={204: "post deleted successfuly"}
    )
	def delete(self, request, pk, format=None):
		post = self.get_object(pk)
		post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)