from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.cache import cache
import re

from .models import TLUser

MAX_ATTEMPTS = 5
BLOCK_TIME = 300  # время блокировки в секундах (5 минут)


def is_blocked(identifier):
    key = f"login_attempts:{identifier}"
    attempts = cache.get(key, 0)
    return attempts >= MAX_ATTEMPTS


def register_attempt(identifier):
    key = f"login_attempts:{identifier}"
    attempts = cache.get(key, 0)
    cache.set(key, attempts + 1, timeout=BLOCK_TIME)


def reset_attempts(identifier):
    cache.delete(f"login_attempts:{identifier}")


def get_client_ip(request):
    """Получение IP адреса из запроса"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class SimpleSignupForm(forms.Form):
    email_or_phone = forms.CharField(label="Email или телефон", max_length=255)
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        min_length=8,
        max_length=64
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтвердите пароль",
        min_length=8,
        max_length=64
    )
    # Поле капчи убрано

    def clean_email_or_phone(self):
        value = self.cleaned_data['email_or_phone'].strip()
        try:
            # Проверяем, что это валидный email
            validate_email(value)
            self.cleaned_data['email'] = value
            self.cleaned_data['tel'] = None
            if TLUser.objects.filter(email=value).exists():
                raise forms.ValidationError("Пользователь с таким email уже существует.")
        except ValidationError:
            # Если не email — проверяем телефон по регулярке
            phone_regex = re.compile(r'^\+?\d{10,15}$')
            if not phone_regex.match(value):
                raise forms.ValidationError("Введите номер телефона в формате +79991234567.")
            if TLUser.objects.filter(tel=value).exists():
                raise forms.ValidationError("Пользователь с таким номером уже существует.")
            self.cleaned_data['tel'] = value
            self.cleaned_data['email'] = None
        return value

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Пароли не совпадают.")

        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', e)

        return cleaned_data

    def save(self):
        email = self.cleaned_data.get('email')
        tel = self.cleaned_data.get('tel')
        password = self.cleaned_data['password']

        user = TLUser(
            email=email,
            tel=tel,
            first_name='',
            last_name='',
            nick=''
        )
        user.set_password(password)
        user.save()
        return user


class TLAuthEmailOrPhoneForm(forms.Form):
    email_or_phone = forms.CharField(label="Email или телефон")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('email_or_phone')
        password = cleaned_data.get('password')

        if not identifier or not password:
            return cleaned_data

        ip = get_client_ip(self.request) if self.request else ''
        identifier_key = f"{ip}:{identifier}"

        if is_blocked(identifier_key):
            raise forms.ValidationError("Слишком много неудачных попыток входа. Повторите позже.")

        user = authenticate(self.request, username=identifier, password=password)

        if not user:
            register_attempt(identifier_key)
            raise forms.ValidationError("Неверный email/телефон или пароль.")

        reset_attempts(identifier_key)
        self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
