from django.contrib import admin
from .models import Manufacturer


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):

    # -------------------------
    # List View
    # -------------------------

    list_display = (
        "code",
        "name",
        "support_email",
        "support_phone",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "support_email",
    )

    list_filter = (
        "is_active",
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
            "Manufacturer Information",
            {
                "fields": (
                    "code",
                    "name",
                    "website",
                    "support_email",
                    "support_phone",
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