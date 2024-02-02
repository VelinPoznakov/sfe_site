from django.urls import path
from .views import home, about, contact, support, register, activate, login_user, logout_user

urlpatterns = [
  path('', home, name='home'),
  path('about-us/', about, name='about-us'),
  path('contact-us/', contact, name='contact-us'),
  path('support/', support, name='support'),
  path('register/', register, name='register'),
  path('activate/<uidb64>/<token>/', activate, name='activate'),
  path('login/', login_user, name='login'),
  path('logout/', logout_user, name='logout'),
  
]

