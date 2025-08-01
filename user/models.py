from django.db import models
from accounts.models import TLUser

class UserProfile(models.Model):
    user = models.OneToOneField(TLUser, on_delete=models.CASCADE, related_name='profile')
    tel = models.CharField(max_length=20, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    nick = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
