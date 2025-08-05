from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from .forms import TLAuthEmailOrPhoneForm, SimpleSignupForm
from .utils import is_registration_enabled
from django.http import HttpResponseForbidden




def register_view(request):
    if not is_registration_enabled():
        return HttpResponseForbidden("Регистрация временно отключена.")


@require_http_methods(["GET", "POST"])
def user_login(request):
    if not getattr(settings, 'AUTH_SYSTEM_ENABLED', True):
        return HttpResponseForbidden("Авторизация временно отключена.")

    if request.user.is_authenticated:
        return redirect('panel:profile')

    if request.method == 'POST':
        form = TLAuthEmailOrPhoneForm(request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('panel:profile')
    else:
        form = TLAuthEmailOrPhoneForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:login')


@require_http_methods(["GET", "POST"])
def register(request):
    if not getattr(settings, 'AUTH_SYSTEM_ENABLED', True):
        return HttpResponseForbidden("Регистрация временно отключена.")

    if request.user.is_authenticated:
        return redirect('panel:profile')

    if request.method == 'POST':
        form = SimpleSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('panel:profile')
    else:
        form = SimpleSignupForm()
    return render(request, 'register.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_email.html'
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
