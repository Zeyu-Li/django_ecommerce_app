"""django_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, 
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView,
)
from login import views as user_views
from shop import views as shop_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shop_views.home, name='home'),
    path('home/', shop_views.home_redirect, name='home_redirect'),
    path('register/', user_views.register, name="register"),
    path('profile/', user_views.profile, name='profile'),
    path('profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('profile/password/', user_views.changepassword, name='changepassword'),
    path('login/', LoginView.as_view(template_name='login/login.html', redirect_authenticated_user=True), name="login"),
]
