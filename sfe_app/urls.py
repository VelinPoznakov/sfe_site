from django.urls import path
from .views import home, about, contact, support

urlpatterns = [
  path('', home, name='home'),
  path('about-us/', about, name='about-us'),
  path('contact-us/', contact, name='contact-us'),
  path('support/', support, name='support'),
  
]

#test

