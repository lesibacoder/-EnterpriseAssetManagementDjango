from django.contrib import admin

from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (

        "department_number",
        "name",
        "manager",
        "location",
        "status",

    )

    search_fields = (

        "department_number",
        "name",
        "manager",

    )

    list_filter = (

        "status",

    )

    readonly_fields = (

        "department_number",
        "created_at",
        "updated_at",

    )

    ordering = (

        "name",

    )

    list_per_page = 20

    fieldsets = (

        (
            "Department Information",
            {
                "fields": (

                    "department_number",

                    "name",

                    "description",

                    "manager",

                    "email",

                    "phone",

                    "location",

                )
            },
        ),

        (
            "Status",
            {
                "fields": (

                    "status",

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