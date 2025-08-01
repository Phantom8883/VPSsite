from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def dashboard(request):
    # Здесь можно добавить логику для сбора данных VPS, уведомлений и т.п.
    return render(request, 'panel/dashboard.html')

@login_required
def profile(request):
    # Здесь можно вывести данные профиля пользователя
    return render(request, 'panel/profile.html')

def home(request):
    return HttpResponse("Главная страница - доступна всем")
