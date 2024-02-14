from django.contrib.auth.models import Group
from django.core.mail import EmailMessage, send_mail
from django.core.mail.backends import smtp
from django.db.models import Q
from sfe_app.forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


def home(request):
    video = AddVideoModel.objects.last()
    video_url = video.video.url if video and video.video.name else None

    context = {
        'video_url': video_url,
        'video': video
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@login_required(redirect_field_name='login', login_url='login')
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
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
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
            if email.send(fail_silently=False):
                messages.success(request, "Activation email sent successfully")
                return redirect('home')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:  # add exeptions
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()

        default_group, _ = Group.objects.get_or_create(name='Default')
        default_group.user_set.add(user)

        messages.success(request, 'You activated your account successfully')
        return redirect('login')
    else:
        messages.error(request, 'Your activation link is invalid')

    return redirect('home')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'User {username} has been successfully logged in')
                return redirect('home')

            else:
                messages.error(request, 'Username or password is incorrect')

    else:
        form = LogInForm()

    return render(request, 'login.html', {'form': form})


@login_required(redirect_field_name='login', login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')


@user_passes_test(is_superuser)
def add_video_view(request):
    if request.method == 'POST':
        form = AddVideoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added video")
            return redirect('home')
    else:
        form = AddVideoForm()

    return render(request, 'add_video.html', {'form': form})


def custom_404(request, exception):
    return redirect('home')


def email_to_send(request):
    if request.method == 'POST':
        form = EnterMailChangePassword(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email'].lower()
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()

            if associated_user:
                mail_subject = "Activate you account"
                message = render_to_string("reset_password_send.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': default_token_generator.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(mail_subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, "Change password email sent successfully")
                else:
                    messages.error(request, 'Error while sending an email')
                return redirect('home')

    else:
        form = EnterMailChangePassword()

    return render(request, 'email_change_password.html', {'form': form})


def change_password(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully")
                return redirect('login')
        else:
            form = ResetPasswordForm(user)

        return render(request, 'reset_password.html', {
            'form': form,
            'uidb64': uidb64,
            'token': token,
        })

    else:
        messages.error(request, 'Your activation link is invalid')

    return redirect('home')


@login_required(login_url='login')
def user_profile(request, pk):
    if request.user.pk == pk:
        user = CustomUser.objects.get(pk=pk)
        return render(request, 'user_profile.html', {'user': user})
    else:
        return redirect('home')


@login_required(login_url='login')
def resend_email_activation(request, pk):
    user = CustomUser.objects.get(pk=pk)
    if not user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        form = EmailChangeForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            if email.lower() != user.email:
                user.email = email.lower()
                user.save()

            mail_subject = "Activate you account email"
            message = render_to_string("account_activation_email.html", {
                'user': user.username,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            if email.send(fail_silently=False):
                messages.success(request, "Activation email sent successfully")
                return redirect('home')

    else:
        form = EmailChangeForm()

        return render(request, 'ver_email_send.html', {'form': form})


def change_username(request, pk):
    user = CustomUser.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = ChangeUsername(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user.username = username
            user.save()
            messages.success(request, f'Your username has been changed successfully to {username}')
            return redirect('home')
        
    else:
        form = ChangeUsername()
        
    return render(request, 'change_username.html', {'form': form})


def change_email(request, pk):
    user = CustomUser.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            user.email = email
            user.save()
            messages.success(request, f'You email has been changed successfully to {email}')
            return redirect('home')
        
    else:
        form = EmailChangeForm()
        
    return render(request, 'email_change.html', {'form': form})


def change_password(request, pk):
    user = CustomUser.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = ResetPasswordForm(user, request.POST)
        
        if form.is_valid():
            print('dsadasd')
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            logout(request)
            messages.success(request, 'Password changed successfully.')
            return redirect('login')          
    else:
        form = ResetPasswordForm(user)
        
    return render(request, 'change_password.html', {'form': form, 'user': user})

            