from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    email = forms.EmailField(label="Digite o email do seu usuário")
    password = forms.CharField(label="Digite a senha do seu usuário", widget=forms.PasswordInput)

    def clean_email(self):
        user = get_user_model()
        email = self.cleaned_data["email"]
        email_exist_or_not = user.objects.filter(email__iexact=email).exists()

        if email_exist_or_not:
            return email

        else: 
            raise ValidationError("E-mail ou senha inválido")


class RegisterForm(forms.Form):
    username = forms.CharField(label="Digite o nome do seu usuário", max_length=150)
    email = forms.EmailField(label="Escolha um e-mail para o seu usuário")
    password = forms.CharField(label="Digite a senha do seu usuário", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirme a senha do seu usuário", widget=forms.PasswordInput)

    def clean_username(self):
        validator = ASCIIUsernameValidator()
        username = self.cleaned_data["username"]
        user = get_user_model()
        username_exist = user.objects.filter(username__iexact=username).exists()

        if validator(username) == None:
            if username_exist:
                raise ValidationError("Nome de usuário já existe na plataforma")    
            else:
                return username 
        else:
            raise ValidationError("Nome inválido, o nome deve ter somente letras")

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = get_user_model()
        email_exist = user.objects.filter(email__iexact=email).exists()

        if email_exist:
            raise ValidationError("E-mail já cadastrado dentro da plataforma")

        else:
            return email
            
        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("password_confirm")

        if password and confirm and password != confirm:
            self.add_error("password_confirm", "Erro, uma senha é diferente da outra!")

        elif password == None:
            raise ValidationError("Sua senha está vázia!")

        elif password:
            try:
                validate_password(password)
            except ValidationError as erro:
                self.add_error("password", erro)

        return cleaned_data
