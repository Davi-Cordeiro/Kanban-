
from django.urls import include, path
from kanban.views import home_view, create_list_view, create_board_view

app_name = 'kanban'

urlpatterns = [
    path('', home_view, name='home'),
    path('board/new', create_board_view, name="criacao_de_painel"),
    path('list/new', create_list_view, name="criacao_de_painel")
]
