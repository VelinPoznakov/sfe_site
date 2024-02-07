from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from sfe_app.models import *
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm


class SupportForm(forms.ModelForm):
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email address', 'class': 'form-control'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={
        'class': 'form-control'}))
    comment_field = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Your comment', 'class': 'form-control'}))

    class Meta:
        model = SupportModel
        fields = ['name', 'email', 'phone_number', 'comment_field']

    def __init__(self, *args, **kwargs):
        super(SupportForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].initial = '+359'

    labels = {
        'name': '',
        'email': '',
        'phone_number': '',
        'comment_field': ''
    }

    def clean_name(self):
        name = self.cleaned_data['name']

        if not name:
            self.add_error('name', 'Please enter a name')

        return name

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email:
            self.add_error('email', 'You have to enter email address')

        try:
            email.split('@')
        except ValueError:
            self.add_error('email', 'Invalid email address')

        return email

    def clean_comment_field(self):
        comment_field = self.cleaned_data['comment_field']

        if not comment_field:
            self.add_error('comment_field', 'You have to enter your comment')

        return comment_field

    def clean_phone_number(self):
        raw_phone_number = self.cleaned_data.get('phone_number')
        if raw_phone_number:
            # Convert the number to E.164 format
            phone_number = to_python(raw_phone_number.as_e164)
            if phone_number and not phone_number.is_valid():
                raise forms.ValidationError("Enter a valid phone number (e.g. +35987157312).")
            return phone_number
        return raw_phone_number


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].required = False
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'

        self.fields['email'].required = False
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter an email'

        self.fields['password1'].required = False
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'

        self.fields['password2'].required = False
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'

    def clean_username(self):
        username = self.cleaned_data['username']
        not_allowed_symbols = ['', '!', '\"', "\'", '#', '%', '@', ',', '$', '^', '&', '*', '(', ')', '-', '=', '_',
                               '~', '+', '`', '<', '>', '?', '[', ']', '{', '}', ':', ';', '|']

        if CustomUser.objects.filter(username=username):
            self.add_error('username', 'This username already exists. Please choose another username.')

        if not username or username is None:
            self.add_error('username', 'You should enter username')

        for el in username:
            if el in not_allowed_symbols:
                self.add_error('username', f'You cannot use {el}')
                break

        if len(username) < 5:
            self.add_error('username', 'You username must be at least 5 characters')

        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if not email or email is None:
            self.add_error('email', 'You should enter an email address')

        if '@' not in email:
            self.add_error('email', 'Please enter a valid email address')

        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', 'This email is already in use. Please choose another email.')

        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']

        if not password1 or password1 is None:
            self.add_error('password1', 'You should enter password')

        if len(password1) < 8:
            self.add_error('password1', 'Password must be at least 8 characters')

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if not password2 or password2 is None:
            self.add_error('password2', 'You must confirm the password')

        if password1 != password2:
            self.add_error('password2', 'The two passwords do not match')

        return password2


class LogInForm(forms.Form):
    username = forms.CharField(max_length=50, label='', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(max_length=128, label='', required=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            self.add_error('username', 'You must enter a username')

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            self.add_error('password', 'You must enter a password')

        return password


class AddVideoForm(forms.ModelForm):
    class Meta:
        model = AddVideoModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddVideoForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = False
        self.fields['name'].label = ''
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter the name of the video'

        self.fields['video'].required = False
        self.fields['video'].label = ''
        self.fields['video'].widget.attrs['placeholder'] = 'Select the video file'
        self.fields['video'].widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name']

        if name is None or not name:
            self.add_error('name', 'You should enter the name of the video')

        return name

    def clean_video(self):
        video = self.cleaned_data['video']

        if video is None or not video:
            self.add_error('video', 'You should upload video')

        return video


class ResetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].label = ''
        self.fields['new_password1'].required = False
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter the new password'

        self.fields['new_password2'].label = ''
        self.fields['new_password2'].required = False
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm the new password'

    def clean(self):
        cleaned_data = super().clean()

        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if not new_password1 or new_password1 is None:
            self.add_error('new_password1', "You should enter a password")

        if not new_password2 or new_password2 is None:
            self.add_error('new_password2', "You should confirm your new password")

        if len(new_password1) < 8:
            self.add_error('new_password1', "Your password must be at least 8 characters")

        if new_password2 != new_password1:
            self.add_error('new_password2', 'The two fields should match')

        return cleaned_data


class EnterMailChangePassword(forms.Form):
    email = forms.CharField(label='', required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter an email'
    }))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if not email or email is None:
            self.add_error('email', "You should enter an email")

        return email
