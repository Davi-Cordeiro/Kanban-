from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    email = forms.EmailField(label="Digite o email do seu usuário")
    password = forms.CharField(label="Digite a senha do seu usuário", widget=forms.PasswordInput)

    def clean_email(self):
        user = get_user_model()
        email = self.cleaned_data["email"]
        email_exist_or_not = user.objects.filter(email__iexact=email).exists()

        if email_exist_or_not == True:
            return email

        else: 
            raise ValidationError("E-mail não existe dentro da plataforma")


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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        confirm = cleaned_data["password_confirm"]

        if password and confirm and password != confirm:
            self.add_error("password_confirm", "Erro, uma senha é diferente da outra!")
        else:
            return cleaned_data
