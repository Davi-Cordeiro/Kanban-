from django.test import TestCase
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model

class RegisterFormTest(TestCase):
    def test_create_user(self):
        form = RegisterForm({"username": "DaviTeste", "email":"teste@gmail.com", "password":"pass@@2025", "password_confirm": "pass@@2025"})
        self.assertTrue(form.is_valid())

    def test_user_duplicated(self):
        #Criando usuário para deixar salvo no banco
        user = get_user_model()
        user_created = user.objects.create_user(username="DaviTeste", email="usernametester@gmail.com", password="usertester@2026")

        
        #Criando usuário com base no forms
        form=RegisterForm({"username":"DaviTeste", "email":"bichomalucotester@gmail.com", "password":"usertester@2026", "password_confirm":"usertester@2026"})
        self.assertFalse(form.is_valid())

    def test_email_duplicated(self):
        #Criando usuário para deixar salvo no banco
        user = get_user_model()
        user_created = user.objects.create_user(username="testedoemail", email="emailtester@gmail.com", password="usertester@2026")
        
        #Criando usuario para testar email repetido
        form = RegisterForm({"username":"testedoemail", "email":"emailtester@gmail.com", "password":"usertester@2026", "password_confirm":"usertester@2026"})
        self.assertIn(form.email, user_created.email)