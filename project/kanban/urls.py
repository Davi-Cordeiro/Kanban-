
from django.urls import include, path
from kanban.views import home_view

app_name = 'kanban'

urlpatterns = [
    path('', home_view, name='home')
]
