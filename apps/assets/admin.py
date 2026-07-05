from django.contrib import admin
from .models import Category, Asset

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    # -------------------------
    # List View (Tree View)
    # -------------------------
    list_display = (
        "id",
        "name",
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "is_active",
        "created_at",
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
            "Category Information",
            {
                "fields": (
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
        "created_at",
        "updated_at",
    )


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = (
        "asset_number",
        "name",
        "category",
        "status",
        "purchase_date",
        "purchase_price",
    )

    search_fields = (
        "asset_number",
        "name",
    )

    list_filter = (
        "status",
        "category",
        "purchase_date",
    )

    ordering = (
        "asset_number",
    )

    list_per_page = 20

    fieldsets = (
        (
            "Asset Information",
            {
                "fields": (
                    "asset_number",
                    "name",
                    "category",
                    "status",
                )
            },
        ),
        (
            "Purchase Information",
            {
                "fields": (
                    "purchase_date",
                    "purchase_price",
                    "warranty_expiry",
                )
            },
        ),
    )

    readonly_fields = (
        "asset_number",
    )