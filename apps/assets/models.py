from django.db import models
from apps.suppliers.models import Supplier
from apps.departments.models import Department
from apps.locations.models import Location
from apps.manufacturers.models import Manufacturer

import qrcode

from io import BytesIO

from django.core.files import File

created_at = models.DateTimeField(auto_now_add=True)


class AssetStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    ASSIGNED = "ASSIGNED", "Assigned"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    DISPOSED = "DISPOSED", "Disposed"
    LOST = "LOST", "Lost",
    DAMAGED = "DAMAGED", "Damaged"


# -------------------------
# Category Model1
# -------------------------
class Category(models.Model):
    """
    Stores asset categories.

    Examples:
    - Laptop
    - Printer
    - Vehicle
    """

    name = models.CharField(
        max_length=100,
        unique=True
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
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

# -------------------------
# Asset Model1
# -------------------------
class Asset(models.Model):

    asset_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="assets"
    )

    name = models.CharField(
        max_length=150
    )
    
    serial_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="assets"
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="assets"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="assets"
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="assets"
    )
    status = models.CharField(
        max_length=20,
        choices=AssetStatus.choices,
        default=AssetStatus.AVAILABLE
    )

    description = models.TextField(
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    asset_image = models.ImageField(
        upload_to="assets/images/",
        blank=True,
        null=True,
    )

    qr_code = models.ImageField(
        upload_to="assets/qrcodes/",
        blank=True,
        null=True,
    )

    purchase_date = models.DateField()

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    warranty_expiry = models.DateField(
        blank=True,
        null=True
    )

    # ============================================================
    # Audit Fields
    # ============================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    def __str__(self):
        return f"{self.asset_number} - {self.name}"
    
    def save(self, *args, **kwargs):

        # Generate Asset Number
        if not self.asset_number:

            last_asset = Asset.objects.order_by("id").last()

            if last_asset:
                last_number = int(
                    last_asset.asset_number.replace(
                        "AST",
                        "",
                    )
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.asset_number = f"AST{next_number:06d}"

        # Save first so we have a primary key
        super().save(*args, **kwargs)

        # Generate QR Code only once
        if not self.qr_code:

            qr = qrcode.make(
                f"http://127.0.0.1:8000/assets/{self.pk}/"
            )

            buffer = BytesIO()

            qr.save(
                buffer,
                format="PNG",
            )

            filename = f"{self.asset_number}.png"

            self.qr_code.save(
                filename,
                File(buffer),
                save=False,
            )

            super().save(update_fields=["qr_code"])