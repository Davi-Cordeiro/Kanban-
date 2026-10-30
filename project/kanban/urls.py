
from django.urls import include, path
from kanban.views import home_view, create_list_view

app_name = 'kanban'

urlpatterns = [
    path('', home_view, name='home'),
    path('creation-painel/', create_list_view, name="criacao-de-view")
]
