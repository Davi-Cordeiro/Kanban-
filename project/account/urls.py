
from django.urls import include, path
from account.views import login_view, logout_view, login_form_view, register_form_view, logout_form_view

urlpatterns = [
    path('login/', login_form_view, name='entrar'),
    path('register/', register_form_view, name='registrar'),
    path('logout/', logout_form_view, name='sair'),
    path("accounts/", include("django.contrib.auth.urls")),
]
