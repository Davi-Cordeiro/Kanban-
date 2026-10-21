from django.db import models
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Digite o email do seu usuário")
    password = forms.CharField(label="Digite a senha do seu usuário", widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(label="Digite o nome do seu usuário", max_length=150)
    email = forms.EmailField(label="Escolha um e-mail para o seu usuário")
    password = forms.CharField(label="Digite a senha do seu usuário", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirme a senha do seu usuário", widget=forms.PasswordInput)
