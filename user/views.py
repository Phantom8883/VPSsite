from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from accounts.models import TLUser
from vps.models import VPS


@login_required(login_url='accounts:login')
def profile(request):
    # Если система авторизации выключена, автоматически логиним тестового пользователя
    if not settings.AUTH_SYSTEM_ENABLED and not request.user.is_authenticated:
        test_user = TLUser.objects.filter(email="test@example.com").first()
        if test_user:
            login(request, test_user)
        else:
            return HttpResponseForbidden("Тестовый пользователь не найден.")

    # Получаем VPS текущего пользователя
    vps_list = VPS.objects.filter(user=request.user).select_related('server')
    return render(request, 'profile.html', {'vps_list': vps_list})
