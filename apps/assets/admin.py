from django.contrib import admin
from .models import Category, Asset

from django.utils.html import format_html
from apps.asset_logs.utils import create_asset_log

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
        "manufacturer",
        "name",
        "serial_number",
        "category",
        "supplier",
        "department",
        "location",
        "status",
        "description",
        "remarks",
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

    @admin.display(description="Image Preview")
    def image_preview(self, obj):

        if obj.asset_image:
            return format_html(
                '<img src="{}" width="150" style="border-radius:8px;" />',
                obj.asset_image.url
            )

        return "-"
    
    @admin.display(description="QR Code")
    def qr_preview(self, obj):

        if obj.qr_code:
            return format_html(
                '<img src="{}" width="150"/>',
                obj.qr_code.url
            )

        return "-"
    
    def save_model(self, request, obj, form, change):

        super().save_model(
            request,
            obj,
            form,
            change,
        )

        if change:

            create_asset_log(
                asset=obj,
                action="Asset Updated",
                user=request.user,
                description="Asset information updated.",
            )

        else:

            create_asset_log(
                asset=obj,
                action="Asset Created",
                user=request.user,
                description="New asset registered.",
            )

    fieldsets = (
        (
            "Asset Information",
            {
                "fields": (
                    "asset_number",
                    "manufacturer",
                    "name",
                    "serial_number",
                    "category",
                    "supplier",
                    "department",
                    "location",
                    "status",
                    "description",
                    "remarks",
                    "asset_image",

                    "image_preview",

                    "qr_code",
                    "qr_preview",
                   
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
        "image_preview",
        "qr_preview",
    )