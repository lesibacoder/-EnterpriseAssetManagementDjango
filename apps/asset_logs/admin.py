from django.contrib import admin

from .models import AssetLog


@admin.register(AssetLog)
class AssetLogAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "action",
        "user",
        "created_at",
    )

    search_fields = (
        "asset__asset_number",
        "action",
    )

    list_filter = (
        "action",
        "created_at",
    )

    ordering = (
        "-created_at",
    )