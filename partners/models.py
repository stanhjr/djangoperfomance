import secrets

from django.db import models


class PartnerConfig(models.Model):
    name = models.CharField(max_length=23)
    description = models.TextField()

    def __str__(self):
        return self.name


class ServiceApiKey(models.Model):
    service_name = models.CharField(
        max_length=200,
    )
    key = models.CharField(
        max_length=200,
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            while True:
                key = secrets.token_hex(32)
                if not ServiceApiKey.objects.filter(key=key).exists():
                    self.key = key
                    break
        super().save(*args, **kwargs)
