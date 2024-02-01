from django.core.mail import EmailMessage

from sfe import settings
from sfe_app.forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


# Create your views here.

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def support(request):
    if request.method == 'POST':

        form = SupportForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been send')
            return redirect('home')

        else:
            messages.error(request, 'Correct the messages below')

    else:
        form = SupportForm()

    return render(request, 'support.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            mail_subject = "Activate you account"
            message = render_to_string("account_activation_email.html", {
                'user': user.username,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(mail_subject, message, to=[form.cleaned_data.get('email')])
            if email.send():
                print('success')
            else:
                print('not success')

            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()

        messages.success(request, 'You activated your account successfully')
        return redirect('home')  # make it to login
    else:
        messages.error(request, 'Your activation link is invalid')

    return redirect('home')

