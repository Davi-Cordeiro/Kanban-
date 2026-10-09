from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    return render(request, 'logout.html')

def home_view(request):
    return render(request, 'home.html')