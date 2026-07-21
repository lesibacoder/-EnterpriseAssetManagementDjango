from django.contrib import admin

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "asset",
        "attachment_type",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "asset__name",
    )

    list_filter = (
        "attachment_type",
    )

    autocomplete_fields = (
        "asset",
    )
    