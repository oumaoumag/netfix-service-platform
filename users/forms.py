from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer
from django.db import transaction



class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


def validate_date_of_birth(value):
    """Ensures date of birth is not beyond 31st December 2008"""
    max_date = date(2008, 12, 31)
    if value > max_date:
        raise ValidationError("Date of Birth must not go beyond 31st December 2008.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        validators=[validate_email],
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d'],
        help_text="Date must not go beyond 31st December 2008.",
        validators=[validate_date_of_birth]
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "date_of_birth"]

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
            Customer.objects.create(user=user, date_of_birth=self.cleaned_data['date_of_birth'])
            return user

        
class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])
    #field = forms.ChoiceField(choices=Company._meta.get_field('field').choices)
    field = forms.ChoiceField(
        choices=Company._meta.get_field('field').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    
    class Meta:
        model = User
        fields = ["username", "email","password1","password2","field"]
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        if commit:
            user.save()
            Company.objects.create(user=user, field=self.cleaned_data["field"])
            return user
       


class UserLoginForm(forms.Form):
   
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
