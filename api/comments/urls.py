from django.shortcuts import render
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from comments import views

urlpatterns = [
	path("", views.CommentList.as_view()),
	path("<str:pk>", views.CommentDetail.as_view())	
]