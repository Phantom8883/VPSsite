from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

from accounts.models import TLUser

class SimpleSignupForm(forms.Form):
    email_or_phone = forms.CharField(label="Email или телефон", max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль", min_length=8, max_length=64)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль", min_length=8, max_length=64)

    def clean_email_or_phone(self):
        value = self.cleaned_data['email_or_phone'].strip()
        try:
            validate_email(value)
            self.cleaned_data['email'] = value
            self.cleaned_data['tel'] = None
            if TLUser.objects.filter(email=value).exists():
                raise forms.ValidationError("Пользователь с таким email уже существует.")
        except ValidationError:
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
