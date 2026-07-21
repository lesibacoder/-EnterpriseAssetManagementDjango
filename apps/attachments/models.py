from django.db import models

from apps.assets.models import Asset
from apps.asset_logs.utils import create_asset_log


class AttachmentType(models.TextChoices):

    PHOTO = "PHOTO", "Photo"

    INVOICE = "INVOICE", "Invoice"

    WARRANTY = "WARRANTY", "Warranty"

    MANUAL = "MANUAL", "Manual"

    SERVICE = "SERVICE", "Service"

    OTHER = "OTHER", "Other"


class Attachment(models.Model):

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    title = models.CharField(
        max_length=200,
    )

    attachment_type = models.CharField(
        max_length=20,
        choices=AttachmentType.choices,
        default=AttachmentType.OTHER,
    )

    file = models.FileField(
        upload_to="attachments/",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:

            create_asset_log(
                asset=self.asset,
                action="Attachment Uploaded",
                description=f"{self.title} uploaded.",
            )

    def __str__(self):

        return self.title

    class Meta:

        ordering = [
            "-uploaded_at",
        ]