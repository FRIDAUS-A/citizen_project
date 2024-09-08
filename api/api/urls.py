"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_swagger.views import get_swagger_view
#from django.conf.urls import url
#from django.conf.urls import url
#from allauth.account.views import confirm_email


schema_view = get_schema_view(
    openapi.Info(
        title="CITIZEN API",
        default_version='v1',
        description="THIS API CONTAINS ALL THE ENPOINT IN THE V1 OF THIS APPLICATION, YOU CAN TEST IT OUT",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="fridausokoya@gmail.com"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

#schema_view_rest = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
	path('api/v1/auth/', include('citizen.urls')),
    path('api/v1/profiles', include('profiles.urls')),
    path('api/v1/posts', include('posts.urls')),
    path('api/v1/comments/', include('comments.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  
]