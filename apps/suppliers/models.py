from django.db import models


class Supplier(models.Model):
    """
    Stores supplier information.
    """

    code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    name = models.CharField(
        max_length=150,
        unique=True
    )

    contact_person = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

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

    def save(self, *args, **kwargs):

        if not self.code:

            last_supplier = Supplier.objects.order_by("id").last()

            if last_supplier:
                last_number = int(last_supplier.code.replace("SUP", ""))
                next_number = last_number + 1
            else:
                next_number = 1

            self.code = f"SUP{next_number:05d}"

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"