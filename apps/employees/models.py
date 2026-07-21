from django.db import models

from apps.departments.models import Department


class EmployeeStatus(models.TextChoices):

    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class Employee(models.Model):

    employee_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    email = models.EmailField(
        unique=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    job_title = models.CharField(
        max_length=100,
    )

    status = models.CharField(
        max_length=20,
        choices=EmployeeStatus.choices,
        default=EmployeeStatus.ACTIVE,
    )

    date_employed = models.DateField()

    profile_picture = models.ImageField(
        upload_to="employees/",
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):

        if not self.employee_number:

            last = Employee.objects.order_by("id").last()

            if last:

                number = int(
                    last.employee_number.replace(
                        "EMP",
                        "",
                    )
                ) + 1

            else:

                number = 1

            self.employee_number = f"EMP{number:06d}"

        super().save(*args, **kwargs)

    @property
    def full_name(self):

        return f"{self.first_name} {self.last_name}"

    def __str__(self):

        return self.full_name

    class Meta:

        ordering = ["first_name", "last_name"]

        verbose_name = "Employee"

        verbose_name_plural = "Employees"