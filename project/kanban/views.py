from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import CardForm, ListForm
from .models import BoardInfo

@login_required
def home_view(request):
    return render(request, 'kanban/home.html')

def create_list_view(request, board_id):
    board = get_object_or_404(BoardInfo, id=board_id)

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.board = board
            position.board = board.lists.count()
            position.save()
            return redirect('home.hmtl')

    else:
        form = ListForm

    return render(request, 'kanban/creation_painel.html', {'form': form})          
