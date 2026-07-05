from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "contact_person",
        "email",
        "phone",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "contact_person",
        "email",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "name",
    )

    list_per_page = 20

    fieldsets = (
        (
            "Supplier Information",
            {
                "fields": (
                    "code",
                    "name",
                    "contact_person",
                    "email",
                    "phone",
                    "address",
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