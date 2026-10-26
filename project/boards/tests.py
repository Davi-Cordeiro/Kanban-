from django.test import TestCase
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model

class RegisterFormTest(TestCase):
    def test_create_user(self):
        form = RegisterForm({"username": "DaviTeste", "email":"teste@gmail.com", "password":"pass@@2025", "password_confirm": "pass@@2025"})
        self.assertTrue(form.is_valid())

    def test_user_duplicated(self):
        #Vendo se o username é repetido
        user = get_user_model()
        user_created = user.objects.create_user(username="DaviTeste", email="usernametester@gmail.com", password="usertester@2026")

        form=RegisterForm({"username":"DaviTeste", "email":"bichomalucotester@gmail.com", "password":"usertester@2026", "password_confirm":"usertester@2026"})
        self.assertFalse(form.is_valid())

    def test_email_duplicated(self):
        #Validação de e-mail é repetido
        user = get_user_model()
        user_created = user.objects.create_user(username="testedoemail", email="emailtester@gmail.com", password="usertester@2026")

        form = RegisterForm({"username":"usuariodoemail", "email":"emailtester@gmail.com", "password":"usertester@2026", "password_confirm":"usertester@2026"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_password_diferent(self):
        #Verificação de senhas diferentes
        form = RegisterForm({"username": "DaviTeste", "email":"teste@gmail.com", "password":"pas@@2025", "password_confirm": "pass@025"})

        self.assertIn("password_confirm", form.errors)
class LoginFormTest(TestCase):
    def test_login_user(self):
        #Validação do login
        form_register = RegisterForm({"username": "DaviTeste", "email":"teste@gmail.com", "password":"pass@@2025", "password_confirm": "pass@@2025"})
        form = LoginForm({"email":"teste@gmail.com", "password": "pass@@2025"})

        self.assertTrue(form.is_valid())

    def test_login_not_exist(self):
        #Analisando para verificar se o usuário existe dentro da plataforma
        form_register = RegisterForm({"username": "DaviTeste", "email":"teste@gmail.com", "password":"pass@@2025", "password_confirm": "pass@@2025"})
        form = LoginForm({"email":"test@gmail.com", "password": "pass@@2025"})

        self.assertFalse(form.is_valid())