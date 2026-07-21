from django import forms

from .models import Department


class DepartmentForm(forms.ModelForm):

    class Meta:

        model = Department

        fields = [

            "name",

            "description",

            "manager",

            "email",

            "phone",

            "location",

            "status",

        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Department name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "manager": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Department manager",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

        }