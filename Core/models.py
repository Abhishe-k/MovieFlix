from django.db import models

from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, User)


# class UserManager(BaseUserManager):
#
#     def create_user(self, username, email, password=None):
#         if username is None:
#             raise TypeError('user should have username')
#
#         if email is None:
#             raise TypeError('user should have an email')
#
#         user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#
#         user.save()
#         return user
#
#     def create_superuser(self, username, email, password=None):
#         if password is None:
#             raise TypeError('Password should not be none')
#
#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#         return user
class UserProfile(models.Model):
    username = models.CharField(max_length=10,unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=10, null=True)
    email = models.EmailField(unique=True, null=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    # objects = UserManager()

    def __str__(self):
        return self.email




