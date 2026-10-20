from django.shortcuts import render
from .models import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView, PasswordResetConfirmView, PasswordResetCompleteView

def login_form_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            usuario = User.objects.filter(email=email).first()
            password = form.cleaned_data['password']

            user = None
            if usuario is not None:
                user = authenticate(request, username=usuario.username, password=password)

            if user is not None:
                login(request, user)
                return render(request, 'home.html', {'form': form})
            form.add_error(None, "Usuário ou email inválido")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_form_view(request):
    logout(request)
    return render(request, 'home.html')


def register_form_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            
            if password == password_confirm:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                return render(request,'home.html', {'form': form})
            
            elif password != password_confirm:
                form.add_error('password_confirm',"Uma senha diferente da outra!")

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form' : form})