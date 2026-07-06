from django.contrib import admin
from .models import AssetModel


@admin.register(AssetModel)
class AssetModelAdmin(admin.ModelAdmin):

    # -------------------------
    # List View
    # -------------------------

    list_display = (
        "code",
        "manufacturer",
        "name",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "manufacturer__name",
    )

    list_filter = (
        "manufacturer",
        "is_active",
    )

    ordering = (
        "manufacturer",
        "name",
    )

    list_per_page = 20

    # -------------------------
    # Form View
    # -------------------------

    fieldsets = (
        (
            "Asset Model Information",
            {
                "fields": (
                    "code",
                    "manufacturer",
                    "name",
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