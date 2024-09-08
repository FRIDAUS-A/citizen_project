from django.shortcuts import render
from comments.models import Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from comments.serializers import CommentSerializer
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
import uuid
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class CommentList(APIView):
	permission_classes = [IsAuthenticated]
	@swagger_auto_schema(
        operation_description="get all comments of the user",
        responses={200: CommentSerializer(many=True)}
    )
	def get(self, request, format=None):
		comments = Comment.objects.filter(citizen_id=request.user.citizen_id)
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)

	@swagger_auto_schema(
        operation_description="create a comment, note that the post field is same as the post_id",
        request_body=CommentSerializer, 
        responses={201: CommentSerializer, 400: 'Bad Request'}
    )
	def post(self, request, format=None):
		permission_classes = [IsAuthenticated]
		user = self.request.user
		data = request.data
		data["citizen"] = user.citizen_id
		data["comment_id"] = str(uuid.uuid4())
		serializer = CommentSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response({"message":"comment created successfully","data": serializer.data}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
	permission_classes = [IsAuthenticated]
	def get_object(self, pk):
		user = self.request.user
		try:
			return Comment.objects.get(pk=pk)
		except Comment.DoesNotExist:
			raise Http404


	@swagger_auto_schema(
        operation_description="get comment with the its id",
        responses={200: CommentSerializer}
    )
	def get(self, request, pk, format=None):
		comment = self.get_object(pk)
		serializer = CommentSerializer(comment)
		return Response(serializer.data)


	@swagger_auto_schema(
        operation_description="update your comment",
        request_body=CommentSerializer, 
        responses={201: CommentSerializer, 400: 'Bad Request'}
    )
	def put(self, request, pk, format=None):
		comment = self.get_object(pk)
		serializer = CommentSerializer(comment, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	


	@swagger_auto_schema(
        operation_description="delete comment using its id",
        responses={204: "comment deleted successfully"}
    )
	def delete(self, request, pk, format=None):
		post = self.get_object(pk)
		post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
