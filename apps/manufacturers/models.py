from django.db import models


class Manufacturer(models.Model):
    """
    Stores asset manufacturers.
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

    website = models.URLField(
        blank=True,
        null=True
    )

    support_email = models.EmailField(
        blank=True,
        null=True
    )

    support_phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
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

    def save(self, *args, **kwargs):

        if not self.code:

            last = Manufacturer.objects.order_by("id").last()

            if last:
                last_number = int(last.code.replace("MFR", ""))
                next_number = last_number + 1
            else:
                next_number = 1

            self.code = f"MFR{next_number:05d}"

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"