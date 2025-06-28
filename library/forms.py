from django import forms
from .models import AdminUser, Book
from django.contrib.auth.forms import AuthenticationForm

class AdminSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = AdminUser
        fields = ['email', 'password']

class AdminLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date']
