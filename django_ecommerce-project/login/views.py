from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from login.forms import (
    RegistrationForm, EditProfileForm
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

def register(request):

# TODO: change redirects to render with messages
    if request.user.is_authenticated:
        extra_context = {'extra_context':{'message':'True','message_title':'Warning: ','message_text':'You are already logged in'}}
        return render(request, 'login/home.html', extra_context)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()
        args = {'form':form}

        return render(request, 'login/register.html', args)


@login_required
def profile(request):
    
    args = {'user':request.user}

    return render(request, 'login/profile.html', args)


@login_required
def edit_profile(request):

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}

        return render(request, 'login/edit_profile.html', args)

@login_required
def changepassword(request):

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')

        else:
            return redirect('changepassword')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}

        return render(request, 'login/changepassword.html', args)
