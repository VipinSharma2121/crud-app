from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, label="Name")
    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2", "image")

