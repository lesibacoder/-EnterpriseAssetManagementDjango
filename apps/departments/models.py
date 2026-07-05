from django.db import models


class Department(models.Model):
    """
    Stores company departments.
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

            last_department = Department.objects.order_by("id").last()

            if last_department:
                last_number = int(last_department.code.replace("DEP", ""))
                next_number = last_number + 1
            else:
                next_number = 1

            self.code = f"DEP{next_number:05d}"

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"