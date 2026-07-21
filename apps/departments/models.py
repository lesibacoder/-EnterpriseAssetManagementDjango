from django.db import models


class DepartmentStatus(models.TextChoices):

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class Department(models.Model):

    department_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    manager = models.CharField(
        max_length=100,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    location = models.CharField(
        max_length=100,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=DepartmentStatus.choices,
        default=DepartmentStatus.ACTIVE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):

        if not self.department_number:

            last = Department.objects.order_by("-id").first()

            if last:

                number = int(last.department_number.replace("DEP", "")) + 1

            else:

                number = 1

            self.department_number = f"DEP{number:06d}"

        super().save(*args, **kwargs)

    @property
    def employee_count(self):

        return self.employees.count()

    def __str__(self):

        return self.name

    class Meta:

        ordering = ["name"]