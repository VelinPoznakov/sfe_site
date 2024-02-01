from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=False)
    date_time_added = models.DateTimeField(auto_now_add=True)


class SupportModel(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200)
    phone_number = PhoneNumberField()
    comment_field = models.CharField(max_length=1000)


# class AddVideo(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50, null=False, blank=False)
#     video = models.FileField(null=False, blank=False)
#     comment = models.TextField(max_length=400, blank=True, null=True)
#     date_time_added = models.DateTimeField(auto_now_add=True)
    
    

