
from django.urls import include, path
from boards.views import login_view, logout_view, home_view
from boards.forms import login_form_view, register_form_view, logout_form_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_form_view, name='login'),
    path('register/', register_form_view, name='register'),
    path('logout/', logout_form_view, name='logout'),
    path("accounts/", include("django.contrib.auth.urls")),
]
