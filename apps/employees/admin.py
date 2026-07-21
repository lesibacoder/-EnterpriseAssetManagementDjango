from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    # -------------------------
    # List View
    # -------------------------

    list_display = (
        "employee_number",
        "full_name",
        "department",
        "job_title",
        "email",
        "phone",
        "status",
        "date_employed",
    )

    search_fields = (
        "employee_number",
        "first_name",
        "last_name",
        "email",
        "job_title",
    )

    list_filter = (
        "status",
        "department",
        "date_employed",
    )

    ordering = (
        "employee_number",
    )

    list_per_page = 20

    # -------------------------
    # Form View
    # -------------------------

    fieldsets = (

        (
            "Employee Information",
            {
                "fields": (
                    "employee_number",
                    "first_name",
                    "last_name",
                    "department",
                    "job_title",
                )
            },
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "phone",
                )
            },
        ),

        (
            "Employment Information",
            {
                "fields": (
                    "status",
                    "date_employed",
                )
            },
        ),

    )

    readonly_fields = (
        "employee_number",
    )