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

class CardForm(forms.ModelForm):
    class Meta:
        model = CardInfo
        fields = ['title', 'description', 'deadline', 'assignee']