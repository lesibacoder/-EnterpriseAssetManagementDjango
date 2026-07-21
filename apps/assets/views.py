from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404, render

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .models import Asset, AssetStatus, Category

from apps.departments.models import Department
from apps.assignments.models import Assignment, AssignmentStatus

from django.core.paginator import Paginator

from .forms import AssetForm

categories = Category.objects.all()

departments = Department.objects.all()


@login_required
def asset_list(request):

    query = request.GET.get("q")
    status = request.GET.get("status")
    category = request.GET.get("category")
    department = request.GET.get("department")

    assets = Asset.objects.select_related(
        "category",
        "department",
        "location",
    )

    if query:

        assets = assets.filter(
            name__icontains=query,
        )

    if status:

        assets = assets.filter(
            status=status,
        )

    if category:

        assets = assets.filter(
            category_id=category,
        )

    if department:

        assets = assets.filter(
            department_id=department,
        )

    assets = assets.order_by(
        "asset_number",
    )

    sort = request.GET.get(
        "sort",
        "asset_number",
    )

    allowed_sort = [
        "asset_number",
        "-asset_number",
        "name",
        "-name",
        "status",
        "-status",
        "category__name",
        "-category__name",
        "department__name",
        "-department__name",
    ]

    if sort not in allowed_sort:
        sort = "asset_number"

    assets = assets.order_by(sort)

    paginator = Paginator(
        assets,
        10,
    )

    page_number = request.GET.get(
        "page",
    )

    assets = paginator.get_page(
        page_number,
    )

    return render(
    request,
    "assets/list.html",
    {
        "assets": assets,
        "categories": categories,
        "departments": departments,
        "statuses": AssetStatus.choices,

        "total_assets": Asset.objects.count(),
        "available_assets": Asset.objects.filter(
            status=AssetStatus.AVAILABLE
        ).count(),
        "assigned_assets": Asset.objects.filter(
            status=AssetStatus.ASSIGNED
        ).count(),
        "maintenance_assets": Asset.objects.filter(
            status=AssetStatus.MAINTENANCE
        ).count(),
        "lost_assets": Asset.objects.filter(
            status=AssetStatus.LOST
        ).count(),
    },
    )

@login_required
def detail(request, pk):

    asset = get_object_or_404(
        Asset,
        pk=pk,
    )

    attachments = asset.attachments.all()

    current_assignment = (
        Assignment.objects
        .filter(
            asset=asset,
            status=AssignmentStatus.ASSIGNED,
        )
        .select_related(
            "employee",
        )
        .first()
    )

    assignment_history = (
        Assignment.objects
        .filter(
            asset=asset,
        )
        .select_related(
            "employee",
        )
        .order_by(
            "-assigned_date",
        )
    )

    return render(
        request,
        "assets/detail.html",
        {
            "asset": asset,
            "attachments": attachments,
            "current_assignment": current_assignment,
            "assignment_history": assignment_history,
        },
    )


@login_required
def edit(request, pk):

    asset = get_object_or_404(
        Asset,
        pk=pk,
    )

    if request.method == "POST":

        form = AssetForm(
            request.POST,
            request.FILES,
            instance=asset,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "asset_detail",
                pk=asset.pk,
            )

    else:

        form = AssetForm(
            instance=asset,
        )

    return render(
        request,
        "assets/edit.html",
        {
            "asset": asset,
            "form": form,
        },
    )