from django.db import models


class AssetStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    ASSIGNED = "ASSIGNED", "Assigned"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    DISPOSED = "DISPOSED", "Disposed"
    LOST = "LOST", "Lost"


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

    name = models.CharField(
        max_length=150
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="assets"
    )

    status = models.CharField(
        max_length=20,
        choices=AssetStatus.choices,
        default=AssetStatus.AVAILABLE
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

    def __str__(self):
        return f"{self.asset_number} - {self.name}"
    
    def save(self, *args, **kwargs):

        if not self.asset_number:

            last_asset = Asset.objects.order_by("id").last()

            if last_asset:
                last_number = int(last_asset.asset_number.replace("AST", ""))
                next_number = last_number + 1
            else:
                next_number = 1

            self.asset_number = f"AST{next_number:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.asset_number} - {self.name}"


    def save(self, *args, **kwargs):

        if not self.asset_number:

            last_asset = Asset.objects.order_by("id").last()

            if last_asset:
                last_number = int(last_asset.asset_number.replace("AST", ""))
                next_number = last_number + 1
            else:
                next_number = 1

            self.asset_number = f"AST{next_number:06d}"

        super().save(*args, **kwargs)



    class Meta:
        ordering = ["asset_number"]