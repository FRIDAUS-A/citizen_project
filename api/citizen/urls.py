from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from citizen import views

urlpatterns = [
    path('', views.CitizenDetail.as_view()),
	path('login/', views.LoginView.as_view(), name='api-login'),
	path('register/', views.RegisterView.as_view(), name='registration-view'),
	path('comment/', views.CommentList.as_view(), name='comment-view'),
	path('posts/', views.ViewPostList.as_view(), name='view-posts'),
	path('post/', views.ViewPostDetail.as_view(), name='view-post'),
    #path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]