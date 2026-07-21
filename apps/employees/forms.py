from django import forms

from .models import Employee
from django.shortcuts import render, get_object_or_404, redirect


class EmployeeForm(forms.ModelForm):

    class Meta:

        model = Employee

        fields = [

            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "job_title",
            "status",
            "date_employed",
            "profile_picture",
            "notes",

        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email address",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone number",
                }
            ),

            "department": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "job_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Job title",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "date_employed": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Additional notes...",
                }
            ),

        }

    def save(self, *args, **kwargs):

        if not self.employee_number:

            last_employee = (
                Employee.objects
                .order_by("-employee_number")
                .first()
            )

            if last_employee:

                last_number = int(
                    last_employee.employee_number.replace("EMP", "")
                )

                self.employee_number = f"EMP{last_number + 1:06d}"

            else:

                self.employee_number = "EMP000001"

        super().save(*args, **kwargs)