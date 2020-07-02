from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash

# django auth backend
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from login.forms import (
    RegistrationForm, EditProfileForm
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


def register(request):
    ''' registers users '''

    # redirect user to home if user is already signed in
    if request.user.is_authenticated:
        extra_context = {'extra_context':{'message':'True','message_title':'Warning: ','message_text':'You are already logged in'}}
        return render(request, 'login/home.html', extra_context)

    # if request is post, redirect to home if it is valid
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        # give user register form
        form = RegistrationForm()
        args = {'form':form}

        return render(request, 'login/register.html', args)


@login_required
def profile(request):
    ''' view profile if logged in '''

    args = {'user':request.user}
    return render(request, 'login/profile.html', args)


@login_required
def edit_profile(request):
    ''' edit profile if logged in '''

    if request.method == 'POST':
        # if post request, check to see if form is valid
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        # give user edit profile form
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'login/edit_profile.html', args)


@login_required
def change_password(request):
    ''' request change in password if user is logged in '''

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')

        else:
            return redirect('change_password')

    else:
        # give user change password form
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}

        return render(request, 'login/change_password.html', args)

# errors, maybe move to different app??
def error_400_view(request, exception):
    return render(request, 'errors/400.html')

def error_403_view(request, exception):
    return render(request, 'errors/403.html')

def error_404_view(request, exception):
    return render(request, 'errors/404.html')

def error_500_view(request):
    return render(request, 'errors/500.html')

