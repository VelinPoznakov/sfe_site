from django.urls import path, re_path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.home, name='home'),
  path('about-us/', views.about, name='about-us'),
  path('contact-us/', views.contact, name='contact-us'),
  path('support/', views.support, name='support'),
  path('register/', views.register, name='register'),
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('login/', views.login_user, name='login'),
  path('logout/', views.logout_user, name='logout'),
  path('add-video/', views.add_video_view, name='add-video'),
  path('email-send/', views.email_to_send, name='email-send'),
  path('change-password/<uidb64>/<token>/', views.change_password, name='reset-password-email'),
  path('profile/<int:pk>/', views.user_profile, name='user-profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'sfe_app.views.custom_404'





