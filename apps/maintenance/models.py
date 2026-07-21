from django.db import models

from apps.assets.models import Asset
from apps.employees.models import Employee
from apps.assets.models import AssetStatus
from django.core.exceptions import ValidationError
from apps.asset_logs.utils import create_asset_log



class MaintenanceStatus(models.TextChoices):

    REPORTED = "REPORTED", "Reported"
    SCHEDULED = "SCHEDULED", "Scheduled"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class MaintenancePriority(models.TextChoices):

    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class Maintenance(models.Model):

    maintenance_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="maintenance_records",
    )

    technician = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="maintenance_jobs",
    )

    priority = models.CharField(
        max_length=20,
        choices=MaintenancePriority.choices,
        default=MaintenancePriority.MEDIUM,
    )

    status = models.CharField(
        max_length=20,
        choices=MaintenanceStatus.choices,
        default=MaintenanceStatus.REPORTED,
    )

    reported_date = models.DateField()

    scheduled_date = models.DateField(
        blank=True,
        null=True,
    )

    completed_date = models.DateField(
        blank=True,
        null=True,
    )

    estimated_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    actual_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    description = models.TextField()

    resolution = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):

        return self.maintenance_number
    

    def clean(self):

        if not self.asset_id:
            return

        exists = Maintenance.objects.filter(
            asset=self.asset,
            status__in=[
                MaintenanceStatus.REPORTED,
                MaintenanceStatus.SCHEDULED,
                MaintenanceStatus.IN_PROGRESS,
            ],
        )

        if self.pk:
            exists = exists.exclude(pk=self.pk)

        if exists.exists():

            raise ValidationError(
                {
                    "asset":
                    "This asset already has an active maintenance request."
                }
            )
        
    def save(self, *args, **kwargs):

        if not self.maintenance_number:

            last = Maintenance.objects.order_by("id").last()

            if last:

                number = int(
                    last.maintenance_number.replace(
                        "MNT",
                        "",
                    )
                ) + 1

            else:

                number = 1

            self.maintenance_number = f"MNT{number:06d}"

        if self.status in (
            MaintenanceStatus.REPORTED,
            MaintenanceStatus.SCHEDULED,
            MaintenanceStatus.IN_PROGRESS,
        ):

            self.asset.status = AssetStatus.MAINTENANCE

        else:

            self.asset.status = AssetStatus.AVAILABLE

        self.asset.save()

        super().save(*args, **kwargs)

        create_asset_log(
            asset=self.asset,
            action="Maintenance",
            description=f"{self.maintenance_number} ({self.status})",
        )

      

class WorkOrder(models.Model):

    maintenance = models.OneToOneField(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="work_order",
    )

    work_done = models.TextField(
        blank=True,
    )

    parts_used = models.TextField(
        blank=True,
    )

    labour_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    technician_notes = models.TextField(
        blank=True,
    )

    completed_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="completed_workorders",
        blank=True,
        null=True,
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):

        return f"WO-{self.maintenance.maintenance_number}"