from django.db import models
from django.conf import settings

class VPS(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vps_instances'
    )
    name = models.CharField(max_length=100, verbose_name="Имя VPS")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    expiration_date = models.DateTimeField(verbose_name="Дата окончания аренды")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.name} ({self.ip_address})"
