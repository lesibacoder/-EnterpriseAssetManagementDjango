from django.db import models

from apps.manufacturers.models import Manufacturer


class AssetModel(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="asset_models"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.manufacturer} {self.name}"

    def save(self, *args, **kwargs):

        if not self.code:

            last = AssetModel.objects.order_by("id").last()

            if last:
                last_number = int(last.code.replace("MOD", ""))
                next_number = last_number + 1
            else:
                next_number = 1

            self.code = f"MOD{next_number:05d}"

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["manufacturer", "name"]
        verbose_name = "Asset Model"
        verbose_name_plural = "Asset Models"