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
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView, LogoutView, 
    PasswordResetView, PasswordResetConfirmView, 
    PasswordResetDoneView, PasswordResetCompleteView,
)
# import both app modules
from login import views as user_views
from shop import views as shop_views

# shop stuff
from shop.views import (
    ItemsView, ItemDetailView, OrderSummaryView, CheckoutView, PaymentView, 
    add_to_cart, remove_from_cart,
    add_single_to_cart, remove_single_from_cart, remove_all_from_cart,
)

# image view
from django.conf import settings
from django.conf.urls.static import static


# admin stuff
admin.site.site_title = 'Database'
admin.site.site_header = 'Red Star Django Admin'
admin.site.index_title = 'Red Star Site Admin'

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
    path('profile/password/', user_views.change_password, name='change_password'),

    # reset password
    path('reset_password/', PasswordResetView.as_view(template_name='login/resetpassword.html', email_template_name='login/reset_password_email.html'), name="password_reset"),
    path('reset_password/done/', PasswordResetDoneView.as_view(template_name='login/text.html'), name="password_reset_done"),
    path('reset_password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='login/change_password.html'), name="password_reset_confirm"),
    # redirect to login
    path('reset_password/complete/', PasswordResetCompleteView.as_view(template_name='shop/home.html'), {'extra_context':{"page": "home", 'message':'True','message_title':'Change Password: ','message_text':'You have successfully changed your password'}}, name="password_reset_complete"),

    # shop
    path('shop/', ItemsView.as_view(), name='item_list'),
    path('shop/product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('shop/add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('shop/remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),

    # after shopping
    path('cart/', login_required(OrderSummaryView.as_view()), name='cart'),
    path('checkout/', login_required(CheckoutView.as_view()), name='checkout'),

    # cart
    path('add_single_to_cart/<slug>/', add_single_to_cart, name='add_single_to_cart'),
    path('remove_single_from_cart/<slug>/', remove_single_from_cart, name='remove_single_from_cart'),
    path('remove_all_from_cart/<slug>/', remove_all_from_cart, name='remove_all_from_cart'),

    # payment
    path('payment/<payment_options>/', login_required(PaymentView.as_view()), name='payment')

]

# errors
handler400 = 'login.views.error_400_view'
handler403 = 'login.views.error_403_view'
handler404 = 'login.views.error_404_view'
handler500 = 'login.views.error_500_view'

# images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)