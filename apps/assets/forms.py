from django import forms

from .models import Asset


class AssetForm(forms.ModelForm):

    class Meta:

        model = Asset

        fields = [
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
            "purchase_date",
            "purchase_price",
            "warranty_expiry",
        ]

        widgets = {

            "manufacturer": forms.Select(attrs={"class": "form-select"}),

            "category": forms.Select(attrs={"class": "form-select"}),

            "supplier": forms.Select(attrs={"class": "form-select"}),

            "department": forms.Select(attrs={"class": "form-select"}),

            "location": forms.Select(attrs={"class": "form-select"}),

            "status": forms.Select(attrs={"class": "form-select"}),

            "name": forms.TextInput(attrs={"class": "form-control"}),

            "serial_number": forms.TextInput(attrs={"class": "form-control"}),

            "purchase_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "purchase_price": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "warranty_expiry": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }