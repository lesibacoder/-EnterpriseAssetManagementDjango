from django.db import models

from apps.assets.models import Asset, AssetStatus
from apps.employees.models import Employee
from django.core.exceptions import ValidationError


class AssignmentStatus(models.TextChoices):

    ASSIGNED = "ASSIGNED", "Assigned"
    RETURNED = "RETURNED", "Returned"


class Assignment(models.Model):

    assignment_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="assignments",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="assignments",
    )

    assigned_date = models.DateField()

    expected_return_date = models.DateField(
        blank=True,
        null=True,
    )

    returned_date = models.DateField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.ASSIGNED,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def clean(self):

        # Asset has not yet been attached (e.g. during form validation)
        if not self.asset_id:
            return

        if self.status == AssignmentStatus.ASSIGNED:

            exists = Assignment.objects.filter(
                asset=self.asset,
                status=AssignmentStatus.ASSIGNED,
            )

            if self.pk:
                exists = exists.exclude(pk=self.pk)

            if exists.exists():

                raise ValidationError(
                    {
                        "asset": (
                            "This asset is already assigned to another employee."
                        )
                    }
                )

        if (
            self.returned_date
            and self.returned_date < self.assigned_date
        ):
            raise ValidationError(
                {
                    "returned_date": (
                        "Returned date cannot be before the assigned date."
                    )
                }
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        if not self.assignment_number:

            last = Assignment.objects.order_by("id").last()

            if last:

                number = int(
                    last.assignment_number.replace(
                        "ASN",
                        "",
                    )
                ) + 1

            else:

                number = 1

            self.assignment_number = f"ASN{number:06d}"

        if self.status == AssignmentStatus.ASSIGNED:

           
            self.asset.status = AssetStatus.ASSIGNED

        else:

            self.asset.status = AssetStatus.AVAILABLE

        self.asset.save()

        super().save(*args, **kwargs)
    

    def __str__(self):

        return self.assignment_number

    class Meta:

        ordering = ["-assigned_date"]