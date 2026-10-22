from django.db import models
from django import forms

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class LoginForm(forms.Form):
    email = forms.EmailField(label="Digite o email do seu usuário")
    password = forms.CharField(label="Digite a senha do seu usuário", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        email.objects.filter(email__iexact.exist())

class RegisterForm(forms.Form):
    username = forms.CharField(label="Digite o nome do seu usuário", max_length=150)
    email = forms.EmailField(label="Escolha um e-mail para o seu usuário")
    password = forms.CharField(label="Digite a senha do seu usuário", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirme a senha do seu usuário", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]

        if username.isalpha():
            return username
        else:
            raise ValidationError("Nome inválido, o nome deve ter somente letras")

    def clean_password(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        password_confirm = cleaned_data["password_confirm"]
        if password != password_confirm:
            self.add_error("password_confirm", "Erro, uma senha é diferente da outra!")
        else:
            return password
