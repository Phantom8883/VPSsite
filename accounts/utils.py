# accounts/utils.py
from .models import SiteSettings

def is_registration_enabled():
    settings = SiteSettings.objects.first()
    return settings and settings.allow_registration
