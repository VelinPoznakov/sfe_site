from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class SupportModel(models.Model):
  name = models.CharField(max_length=80)
  email = models.EmailField(max_length=200)
  phone_number = PhoneNumberField()
  coment_field = models.CharField(max_length=1000)
  
  