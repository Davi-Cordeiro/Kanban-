from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import CardForm, ListForm, BoardForm
from .models import BoardInfo

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
            return redirect('kanban:home')

    else:
        form = ListForm()

    return render(request, 'kanban/creation_list.html', {'form': form})          

def board_detail_view(request, board_id):
    board = get_object_or_404(BoardInfo, pk=board_id)
    lista = board.lists.order_by('position').prefetch_related('cards','card__labels')
    return render(request, "kanban/board_detail.html", {'board': board, 'listas': lista} )