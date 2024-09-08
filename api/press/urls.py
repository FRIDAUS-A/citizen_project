from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from press import views

urlpatterns = [
    path('', views.PressDetail.as_view()),
	path('login/', views.LoginView.as_view(), name='api-login'),
	path('register/', views.RegisterView.as_view(), name='registration-view'),
	path('posts/', views.PressPostList.as_view(), name="press-posts"),
	path('post/<str:pk>', views.PressPostDetail.as_view(), name="press-post"),
	
    #path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]