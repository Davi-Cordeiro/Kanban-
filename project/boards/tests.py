from django.test import TestCase
from django.urls import reverse
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
        self.assertIn("username", form.errors)

    def test_email_duplicated(self):
        #Validação de e-mail é repetido
        user = get_user_model()
        user_created = user.objects.create_user(username="testedoemail", email="emailtester@gmail.com", password="usertester@2026")

        form = RegisterForm({"username":"usuariodoemail", "email":"emailtester@gmail.com", "password":"usertester@2026", "password_confirm":"usertester@2026"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_password_weak(self):
        #Analisa se a senha é fraca
        form = RegisterForm({"username": "DaviTeste", "email":"teste@gmail.com", "password":"123", "password_confirm": "123"})

        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_username_duplicated(self):
        #Analisa se o username foi escrito em maiusculo/usernames diferentes
        user = get_user_model()
        user_created = user.objects.create_user(username="DaviTeste", email="usernametester@gmail.com", password="usertester@2026")
        
        form = RegisterForm({"username": "DAVITESTE", "email":"teste@gmail.com", "password":"pass@@2025", "password_confirm": "pass@@2025"})
        self.assertIn("username", form.errors)

    def test_email_diferent_letters(self):
        #Avisa caso o email tenha letra diferentes dos que estão no banco
        user = get_user_model()
        user_created = user.objects.create_user(username="DaviTeste", email="usernametester@gmail.com", password="usertester@2026")

        form = RegisterForm({"username": "DaviTeste", "email":"teste@gmail.com", "password":"pass@@2025", "password_confirm": "pass@@2025"})
        self.assertIn("email", form.errors)
    def test_password_error(self):
        #Verifica uma senha diferente da outra
        form = RegisterForm({"username": "DaviTeste", "email":"teste@gmail.com", "password":"pas@@2025", "password_confirm": "pass@025"})

        self.assertIn("password_confirm", form.errors)

    def test_username_error(self):
        # Validação no username
        form = RegisterForm({"username":" 'u'suariodo   email", "email":"emailtester@gmail.com", "password":"usertester@2026", "password_confirm":"usertester@2026"})

        self.assertIn("username", form.errors)


class LoginFormTest(TestCase):
    def test_login_user(self):
        #Validação do login
        user = get_user_model()
        user_created = user.objects.create_user(username="testedoemail", email="emailtester@gmail.com", password="usertester@2026")
        form = LoginForm({"email":"emailtester@gmail.com", "password": "usertester@2026"})

        self.assertTrue(form.is_valid())

    def test_login_not_exist(self):
        #Analisando para verificar se o usuário existe dentro da plataforma
        form = LoginForm({"email":"test@gmail.com", "password": "pass@@2025"})

        self.assertFalse(form.is_valid())


class AuthViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="DaviTeste", email="teste@gmail.com", password="pass@@2025")

    def test_register_view_create_user(self):
        response = self.client.post(reverse("registrar"), {"username": "NovoUser","email": "novo@gmail.com", "password": "pass@@2025", "password_confirm": "pass@@2025" })

        self.assertRedirects(response, reverse("Home"))