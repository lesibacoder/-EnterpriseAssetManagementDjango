from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    # -------------------------
    # List View
    # -------------------------

    list_display = (
        "code",
        "name",
        "building",
        "floor",
        "room",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "building",
        "room",
    )

    list_filter = (
        "is_active",
        "building",
    )

    ordering = (
        "name",
    )

    list_per_page = 20

    # -------------------------
    # Form View
    # -------------------------

    fieldsets = (
        (
            "Location Information",
            {
                "fields": (
                    "code",
                    "name",
                    "building",
                    "floor",
                    "room",
                    "description",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                )
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "code",
        "created_at",
        "updated_at",
    )