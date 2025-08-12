from django import forms
from django.contrib.auth import authenticate
from accounts.forms.security import is_blocked, register_attempt, reset_attempts, get_client_ip

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
