from .models import BoardInfo, LabelInfo, ListInfo, CardInfo
from django import forms

class BoardForm(forms.ModelForm):
    class Meta:
        model =  BoardInfo
        fields = ['title']

class LabelForm(forms.ModelForm):
    class Meta:
        model = LabelInfo
        fields =  ['name', 'color']

class ListForm(forms.ModelForm):
    class Meta:
        model = ListInfo
        fields = ['title']
        labels = {'title': 'Nome da etapa',}

class CardForm(forms.ModelForm):
    class Meta:
        model = CardInfo
        fields = ['title', 'description', 'list', 'assignee']

    def __init__(self, *args, board=None, **kwargs):
        super().__init__(*args, **kwargs)
        if board:
            self.fields['assignee'].queryset = board.members.all()
            self.fields['list'].queryset = board.lists.all()