from django import forms

from .models import Assignment


class AssignmentForm(forms.ModelForm):

    class Meta:

        model = Assignment

        fields = (

            "employee",
            "assigned_date",
            "expected_return_date",
            "notes",

        )

        widgets = {

            "employee": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "assigned_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "expected_return_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

        }