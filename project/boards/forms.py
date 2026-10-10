from django.shortcuts import render
from .models import LoginForm, RegisterForm
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return render(request, 'home.html', {form: form})
    else:
        form = LoginForm()
        return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            return render(request,'home.html', {form: form})
        else:
            return render(request, 'register.html')