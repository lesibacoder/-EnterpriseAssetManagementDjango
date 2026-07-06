from django.db import models


class Location(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    name = models.CharField(
        max_length=150,
        unique=True
    )

    building = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    floor = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    room = models.CharField(
        max_length=50,
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

            last_location = Location.objects.order_by("id").last()

            if last_location:
                last_number = int(last_location.code.replace("LOC", ""))
                next_number = last_number + 1
            else:
                next_number = 1

            self.code = f"LOC{next_number:05d}"

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"