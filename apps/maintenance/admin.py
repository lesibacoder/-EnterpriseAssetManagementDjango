from django.contrib import admin

from .models import Maintenance, WorkOrder


class WorkOrderInline(admin.StackedInline):

    model = WorkOrder

    extra = 0

    max_num = 1

    can_delete = False


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):

    list_display = (
        "maintenance_number",
        "asset",
        "technician",
        "priority",
        "status",
        "reported_date",
    )

    search_fields = (
        "maintenance_number",
        "asset__asset_number",
        "asset__name",
    )

    list_filter = (
        "status",
        "priority",
        "reported_date",
    )

    ordering = (
        "-reported_date",
    )

    readonly_fields = (
        "maintenance_number",
    )

    inlines = (
        WorkOrderInline,
    )

    fieldsets = (
    (
        "Maintenance Information",
        {
            "fields": (
                "maintenance_number",
                "asset",
                "technician",
                "priority",
                "status",
            )
        },
    ),
    (
        "Dates",
        {
            "fields": (
                "reported_date",
                "scheduled_date",
                "completed_date",
            )
        },
    ),
    (
        "Costs",
        {
            "fields": (
                "estimated_cost",
                "actual_cost",
            )
        },
    ),
    (
        "Details",
        {
            "fields": (
                "description",
                "resolution",
            )
        },
    ),
)