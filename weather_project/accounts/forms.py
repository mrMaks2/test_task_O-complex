from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email') # Укажите поля, которые хотите видеть в форме

class LoginForm(AuthenticationForm):
    pass