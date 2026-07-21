from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from apps.assets.models import Asset
from .models import Assignment

from .forms import AssignmentForm

from django.contrib import messages

from django.utils import timezone

from .models import AssignmentStatus



def checkout_asset(request, pk):

    asset = get_object_or_404(
        Asset,
        pk=pk,
    )

    if asset.status == "ASSIGNED":

        messages.error(
            request,
            "This asset is already assigned to an employee.",
        )

        return redirect(
            "asset_detail",
            pk=asset.pk,
        )

    if request.method == "POST":

        form = AssignmentForm(
            request.POST,
        )

        if form.is_valid():

            assignment = form.save(
                commit=False,
            )

            assignment.asset = asset

            assignment.save()

            return redirect(
                "asset_detail",
                pk=asset.pk,
            )

    else:

        form = AssignmentForm()

    return render(
        request,
        "assignments/checkout.html",
        {
            "asset": asset,
            "form": form,
        },
    )

def return_asset(request, pk):

    asset = get_object_or_404(
        Asset,
        pk=pk,
    )

    assignment = Assignment.objects.filter(
        asset=asset,
        status=AssignmentStatus.ASSIGNED,
    ).first()

    if assignment:

        assignment.status = AssignmentStatus.RETURNED

        assignment.returned_date = timezone.now().date()

        assignment.save()

    return redirect(
        "asset_detail",
        pk=asset.pk,
    )