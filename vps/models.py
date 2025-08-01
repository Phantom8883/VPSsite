from django.db import models
from accounts.models import TLUser
from datetime import timedelta

class VPS(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    # любые дополнительные поля, возможно миграция из SQL

class VPSRent(models.Model):
    user = models.ForeignKey(TLUser, on_delete=models.CASCADE)
    vps = models.ForeignKey(VPS, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)
