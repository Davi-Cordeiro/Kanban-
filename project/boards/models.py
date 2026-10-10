from django.db import models
from django import forms

# Usuário
#  └── Quadro (Board)      título, dono, membros, data de criação
#       ├── Etiqueta (Label)   nome, cor
#       └── Lista (List)       título, posição
#            └── Cartão (Card) título, descrição, prazo, etiquetas, responsável, posição
# ```

class BoardInfo(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField('auth.User', related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class LabelInfo(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)  # Cor em formato hexadecimal (ex: #FF0000)
    board = models.ForeignKey(BoardInfo, on_delete=models.CASCADE, related_name='labels')

    def __str__(self):
        return self.name

class ListInfo(models.Model):
    title = models.CharField(max_length=100)
    position = models.PositiveIntegerField()
    board = models.ForeignKey(BoardInfo, on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return self.title

class CardInfo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=600)
    deadline = models.DateTimeField(null=True, blank=True)
    position = models.PositiveIntegerField()
    list = models.ForeignKey(ListInfo, on_delete=models.CASCADE, related_name='cards')
    labels = models.ManyToManyField(LabelInfo, related_name='cards', blank=True)
    assignee = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='assigned_cards')

    def __str__(self):
        return self.title
class LoginForm(forms.Form):
    email = forms.EmailField("Digite o email do seu usuário")
    password = forms.CharField("Digite a senha do seu usuário", widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField("Digite o nome do seu usuário", max_length=150)
    email = forms.EmailField("Escolha um e-mail para o seu usuário")
    password = forms.CharField("Digite a senha do seu usuário", widget=forms.PasswordInput)
    password_confirm = forms.CharField("Confirme a senha do seu usuário", widget=forms.PasswordInput)
