from django.shortcuts import render
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views

urlpatterns = [
	path("", views.PostList.as_view()),
	path("<str:pk>", views.PostDetail.as_view())	
]