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
    PasswordResetConfirmView, PasswordResetDoneView, 
    PasswordResetCompleteView, PasswordChangeView
)
# import both app modules
from login import views as user_views
from shop import views as shop_views
# TODO: https://www.youtube.com/watch?v=Xjty8q524Jo (14:00)


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # home views
    path('', shop_views.home, name='home'),
    path('home/', shop_views.home_redirect, name='home_redirect'),

    # login
    path('login/', LoginView.as_view(template_name='login/login.html', redirect_authenticated_user=True), name="login"),
    path('register/', user_views.register, name="register"),

    # logout
    path('logout/', LogoutView.as_view(template_name='shop/home.html'), {'extra_context':{"page": "home", 'message':'True','message_title':'Logout: ','message_text':'You have logged out successfully'}}, name="logout"),

    # user profile
    path('profile/', user_views.profile, name='profile'),
    path('profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('profile/password/', PasswordChangeView.as_view(template_name='login/change_password.html',), name='change_password'),

    # reset password
    path('reset_password/', PasswordResetView.as_view(template_name='login/resetpassword.html', email_template_name='login/reset_password_email.html'), name="password_reset"),
    path('reset_password/done/', PasswordResetDoneView.as_view(template_name='login/text.html'), name="password_reset_done"),
    path('reset_password/complete/', PasswordResetCompleteView.as_view(template_name='login/home.html'), name="password_reset_complete"),
    path('reset_password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='login/resetpassword.html'), name="password_reset_confirm"),
]

# errors
handler400 = 'login.views.error_400_view'
handler403 = 'login.views.error_403_view'
handler404 = 'login.views.error_404_view'
handler500 = 'login.views.error_500_view'
