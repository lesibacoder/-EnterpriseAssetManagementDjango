from django.db import models

from django.contrib.auth import get_user_model

from apps.assets.models import Asset

User = get_user_model()


class AssetLog(models.Model):

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="logs",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return f"{self.asset.asset_number} - {self.action}"