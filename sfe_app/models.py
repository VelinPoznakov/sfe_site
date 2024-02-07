from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=100, unique=True)
    is_email_verified = models.BooleanField(default=False)
    date_time_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Convert email to lowercase before saving
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class SupportModel(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200)
    phone_number = PhoneNumberField()
    comment_field = models.CharField(max_length=1000)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class AddVideoModel(models.Model):
    name = models.CharField(max_length=30)
    video = models.FileField(upload_to='videos/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name







    
    

