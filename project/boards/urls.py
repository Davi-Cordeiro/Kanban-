
from django.urls import include, path
from boards.views import login_view, logout_view, home_view, login_form_view, register_form_view, logout_form_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_form_view, name='entrar'),
    path('register/', register_form_view, name='registrar'),
    path('logout/', logout_form_view, name='sair'),
    path("accounts/", include("django.contrib.auth.urls")),
]
