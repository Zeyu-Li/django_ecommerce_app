from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField


class RegistrationForm(UserCreationForm):
    ''' registration for the website '''

    email = forms.EmailField(required=True)
    captcha = ReCaptchaField(label='')

    # data retaining to creating a new user, including there username, 
    # first and last name, email, password, password confirmation, and recaptcha
    class Meta:
        model = User
        fields = (
            'username',
            'first_name', # optional
            'last_name', # optional
            'email',
            'password1',
            'password2', # password confirmation
            'captcha'
        )

    def save(self, commit=True):
        # save registration to user in database
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # if successful, save the user to database
        if commit:
            user.save()

        return user


class EditProfileForm(forms.ModelForm):
    ''' editting a profile '''

    class Meta:
        ''' you can only change your email, first and last name when editing your profile '''
        model = User
        fields = (
            'email',
            'first_name',
            'last_name'
        )
