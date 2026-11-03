import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import CardForm, ListForm, BoardForm
from .models import BoardInfo, ListInfo

@login_required
def home_view(request):
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
    board = get_object_or_404(BoardInfo, pk=board_id)

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


@login_required
def board_detail_view(request, board_id):

    try:

        if request.method == 'POST':

            dados = json.loads(request.body)

            list_id = dados.get('list_id')

            if dados.get('action') == 'edit_list':
                new_title = dados.get('new_title')

                if new_title is None:
                    return JsonResponse({'error': 'Título não encontrado.'}, status=404)
            
                elif new_title:
                    lista = get_object_or_404(ListInfo, pk=list_id, request=request.user)
                    lista.title = new_title.strip()
                    lista.save(update_fields=['title'])
                    return JsonResponse({'message': 'Lista atualizada com sucesso.', 'title': lista.title})

                elif new_title == '':
                    return JsonResponse({'error': 'O título da lista não pode estar vazio.'}, status=400)

                else: 
                    return JsonResponse({'error': 'O título da lista deve conter apenas letras.'}, status=400)
                                    
            elif dados.get('action') == 'delete_list':
                lista = get_object_or_404(ListInfo, pk=list_id)
                lista.delete()
                return JsonResponse({'message': 'Lista deletada com sucesso.'})

    
            

        board = get_object_or_404(BoardInfo, pk=board_id)
        listas = board.lists.order_by('position').prefetch_related('cards','cards__labels')
        
        return render(request, "kanban/board_detail.html", {'board': board, 'listas': listas} )
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Requisição inválida.'}, status=400)