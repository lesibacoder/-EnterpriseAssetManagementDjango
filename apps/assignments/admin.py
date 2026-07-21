from django.contrib import admin

from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    # ---------------------------------
    # List View
    # ---------------------------------

    list_display = (
        "assignment_number",
        "asset",
        "employee",
        "assigned_date",
        "expected_return_date",
        "returned_date",
        "status",
    )

    search_fields = (
        "assignment_number",
        "asset__asset_number",
        "asset__name",
        "employee__first_name",
        "employee__last_name",
    )

    list_filter = (
        "status",
        "assigned_date",
        "returned_date",
        "employee__department",
    )

    ordering = (
        "-assigned_date",
    )

    list_per_page = 20

    # ---------------------------------
    # Form Layout
    # ---------------------------------

    fieldsets = (

        (
            "Assignment Information",
            {
                "fields": (
                    "assignment_number",
                    "asset",
                    "employee",
                    "status",
                )
            },
        ),

        (
            "Assignment Dates",
            {
                "fields": (
                    "assigned_date",
                    "expected_return_date",
                    "returned_date",
                )
            },
        ),

        (
            "Additional Information",
            {
                "fields": (
                    "notes",
                )
            },
        ),

    )

    readonly_fields = (
        "assignment_number",
    )