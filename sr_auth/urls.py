"""sr_auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login_redirect/', views.login_redirect,
         name='login_redirect'),
    
    
    #Auth
    path('get_auth_enabled/<str:product_name>',
         views.get_auth_enabled, name='get_auth_enabled'),
    path('can_use_redirect/<str:product_name>',
         views.can_use_redirect, name='can_use_redirect'),

    
    #RAuth REST API
    path('can_use/<str:product_name>', views.can_use, name='can_use'),
    path('auth_status/<str:product_name>',
         views.auth_status, name='auth_status'),
    path('enable_auth/<str:product_name>',
         views.enable_auth, name='enable_auth'),

]
