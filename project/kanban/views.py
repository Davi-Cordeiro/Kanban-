import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import CardForm, ListForm, BoardForm
from .models import BoardInfo, ListInfo


def edit_board(request, dados):
    board = BoardInfo.objects.filter(pk=dados.get('board_id'), owner=request.user).first()

    if board is None:
        return JsonResponse({'error': 'Quadro não encontrado ou sem permissão.'}, status=404)

    title = (dados.get('new_title') or '').strip()
    if not title or len(title) > 100:
        return JsonResponse({'error': 'O título deve ter entre 1 e 100 caracteres.'}, status=400)

    board.title = title
    board.save(update_fields=['title'])
    return JsonResponse({'title': board.title})


def delete_board(request, dados):
    board = get_object_or_404(BoardInfo, pk=dados.get('board_id'), owner=request.user)
    board.delete()
    return JsonResponse({'ok': True})


ACTIONS_BOARD = {
    'edit_board': edit_board,
    'delete_board': delete_board,
}


@login_required
def home_view(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Requisição inválida.'}, status=400)

        handler = ACTIONS_BOARD.get(dados.get('action'))
        if handler is None:
            return JsonResponse({'error': 'Ação desconhecida.'}, status=400)

        return handler(request, dados)

    boards = BoardInfo.objects.filter(members=request.user)
    return render(request, 'home.html', {'boards': boards})

@login_required
def create_board_view(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()    
            board.members.add(request.user)
            return redirect ('kanban:home')

    else:
        form = BoardForm()

    return render(request, 'kanban/creation_painel.html', {'form': form})

@login_required
def create_list_view(request, board_id):
    board = get_object_or_404(BoardInfo, pk=board_id, members=request.user)

    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            lista = form.save(commit=False)
            lista.board = board
            lista.position = board.lists.count()
            lista.save()
            return redirect('kanban:board_detail', board_id=board.id)

    else:
        form = ListForm()

    return render(request, 'kanban/creation_list.html', {'form': form})          


def edit_list_view(request, dados, list_id):
    title = dados.get('new_title')
    if title is None:
        return JsonResponse({'error': 'Título vazio, escreva novamente'})
    if not title or len(title) > 100:
        return JsonResponse({'error': 'O Título tem que ser menor que 100 caractere e maior que 1 caractere'})

    lista = get_object_or_404(ListInfo, pk=list_id, board__members=request.user)
    new_title = dados.get('new_title')
    lista.title = new_title.strip()
    lista.save(update_fields=['title'])
    return JsonResponse({'message': 'Lista atualizada com sucesso', 'title': lista.title}, status=200)


def delete_list_view(request, dados, list_id):

    lista = get_object_or_404(ListInfo, pk=list_id)
    lista.delete()
    return JsonResponse({'message': 'Etapa removida com sucesso'})

ACTIONS_LIST = {
    'edit_list': edit_list_view,
    'delete_list': delete_list_view
}

    
@login_required
def board_detail_view(request, board_id):
    board = get_object_or_404(BoardInfo, pk=board_id, members=request.user)

    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            list_id = dados.get('list_id')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Requisição inválida.'}, status=400)
        
        handler = ACTIONS_LIST.get(dados.get('action'))

        if handler is None:
            return JsonResponse({'error': 'Requisição com dados inexistentes'}, status=400)

        return handler(request, dados, list_id)
        

    board = get_object_or_404(BoardInfo, pk=board_id, members=request.user)
    listas = board.lists.order_by('position').prefetch_related('cards','cards__labels')
    
    return render(request, "kanban/board_detail.html", {'board': board, 'listas': listas} )
        