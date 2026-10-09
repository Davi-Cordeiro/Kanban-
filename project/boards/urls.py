from django.contrib import admin
from django.urls import include, path

from boards.views import login_view, logout_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
