from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from sfe_app.models import *
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from phonenumber_field.phonenumber import to_python
from django.contrib.auth.forms import UserCreationForm


class SupportForm(forms.ModelForm):
    name = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email address', 'class': 'form-control'}))
    phone_number = PhoneNumberField()
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
        self.fields['email'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False

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
        email = self.cleaned_data['email']

        if not email or email is None:
            self.add_error('email', 'You should enter an email address')

        if '@' not in email:
            self.add_error('email', 'Please enter a valid email address')

        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', 'This email is already in use. Please choose another email.')

        return email


class ResendActivationLinkForm(forms.Form):  # remake
    email = forms.EmailField(label='Your email address', max_length=100, help_text='Enter the email address you used '
                                                                                   'for registration.')
