from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    ''' a model referencing a user, contains the user and the email '''

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    email = models.EmailField(max_length=70, default='')

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    ''' create an instance of user '''

    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

# save to datbase
post_save.connect(create_profile, sender=User)
