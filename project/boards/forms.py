from django.shortcuts import render
from .models import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_form_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            usuario = User.get(filter(email=email).first())
            password = form.cleaned_data['password']
            user = authenticate(request,username=usuario.username, email=email, password=password)
            if user is not None:
                login(request, user)
                form.add_error("Usuário ou email inválido")
                return render(request, 'home.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

        
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
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form' : form})