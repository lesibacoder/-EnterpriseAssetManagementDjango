from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from apps.assets.models import Asset
from apps.departments.models import Department
from apps.locations.models import Location
from apps.manufacturers.models import Manufacturer
from apps.suppliers.models import Supplier

from django.db.models.functions import TruncMonth


@login_required
def index(request):
    """
    ============================================================
    Enterprise Dashboard

    Displays:
    - Dashboard Header
    - KPI Cards
    - Charts
    - Recent Activity
    - Warranty Alerts

    ============================================================
    """

    # ============================================================
    # Dashboard Date Information
    # ============================================================

    today = timezone.now().date()

    next_30_days = today + timedelta(days=30)

    # ============================================================
    # Dashboard Greeting
    # ============================================================

    current_hour = timezone.localtime().hour

    if current_hour < 12:
        greeting = "Good Morning"

    elif current_hour < 18:
        greeting = "Good Afternoon"

    else:
        greeting = "Good Evening"

    # ============================================================
    # Dashboard Statistics
    # ============================================================

    total_assets = Asset.objects.count()

    total_departments = Department.objects.count()

    total_suppliers = Supplier.objects.count()

    total_manufacturers = Manufacturer.objects.count()

    total_locations = Location.objects.count()

    # ============================================================
    # Asset Status Counts
    # ============================================================

    available_assets = Asset.objects.filter(
        status="AVAILABLE"
    ).count()

    assigned_assets = Asset.objects.filter(
        status="ASSIGNED"
    ).count()

    maintenance_assets = Asset.objects.filter(
        status="MAINTENANCE"
    ).count()

    damaged_assets = Asset.objects.filter(
        status="DAMAGED"
    ).count()

    # ============================================================
    # Asset Percentages
    # ============================================================

    if total_assets > 0:

        available_percent = round(
            (available_assets / total_assets) * 100
        )

        assigned_percent = round(
            (assigned_assets / total_assets) * 100
        )

        maintenance_percent = round(
            (maintenance_assets / total_assets) * 100
        )

        damaged_percent = round(
            (damaged_assets / total_assets) * 100
        )

    else:

        available_percent = 0

        assigned_percent = 0

        maintenance_percent = 0

        damaged_percent = 0

    # ============================================================
    # Asset Health Score
    #
    # Calculates the overall operational health of company assets.
    #
    # Formula:
    # Healthy Assets = Available + Assigned
    # Health Score = Healthy Assets / Total Assets
    # ============================================================

    healthy_assets = available_assets + assigned_assets

    if total_assets > 0:

        asset_health_score = round(
            (healthy_assets / total_assets) * 100
        )

    else:

        asset_health_score = 0

    # ============================================================
    # Monthly Asset Growth
    #
    # Displays the number of assets registered each month.
    # Used by the dashboard line chart.
    # Monthly Asset Growth
    #
    # PostgreSQL version
    # ============================================================

    monthly_growth = (

        Asset.objects

        .annotate(month=TruncMonth("created_at"))

        .values("month")

        .annotate(total=Count("id"))

        .order_by("month")

    )

    # ============================================================
    # Dashboard Notifications
    #
    # Used by the Notification Center widget.
    # ============================================================

    notification_counts = {

        "warranty": Asset.objects.filter(
            warranty_expiry__isnull=False,
            warranty_expiry__lte=next_30_days,
            warranty_expiry__gte=today,
        ).count(),

        "maintenance": maintenance_assets,

        "recent_assets": Asset.objects.filter(
            created_at__date=today
        ).count(),

        "assigned": assigned_assets,

    }

    # ============================================================
    # Dashboard Context
    # ============================================================

    context = {

        # --------------------------------------------------------
        # Dashboard Header
        # --------------------------------------------------------

        "greeting": greeting,

        "today": timezone.now(),

        # --------------------------------------------------------
        # Statistics
        # --------------------------------------------------------

        "total_assets": total_assets,

        "total_departments": total_departments,

        "total_suppliers": total_suppliers,

        "total_manufacturers": total_manufacturers,

        "total_locations": total_locations,

        # --------------------------------------------------------
        # Asset Status
        # --------------------------------------------------------

        "available_assets": available_assets,

        "assigned_assets": assigned_assets,

        "maintenance_assets": maintenance_assets,

        "damaged_assets": damaged_assets,

        # --------------------------------------------------------
        # Asset Percentages
        # --------------------------------------------------------

        "available_percent": available_percent,

        "assigned_percent": assigned_percent,

        "maintenance_percent": maintenance_percent,

        "damaged_percent": damaged_percent,

        "monthly_growth": monthly_growth,

        # --------------------------------------------------------
        # Notifications
        # --------------------------------------------------------

        "notifications": notification_counts,

        # --------------------------------------------------------
        # Asset Health
        # --------------------------------------------------------

        "healthy_assets": healthy_assets,

        "asset_health_score": asset_health_score,

        # --------------------------------------------------------
        # Recent Records
        # --------------------------------------------------------

        "recent_assets": Asset.objects.select_related(
            "category"
        ).order_by("-id")[:5],

        "recent_suppliers": Supplier.objects.order_by("-id")[:5],

        # --------------------------------------------------------
        # Charts
        # --------------------------------------------------------

        "category_chart": (
            Asset.objects
            .values("category__name")
            .annotate(total=Count("id"))
            .order_by("category__name")
        ),

        "status_chart": (
            Asset.objects
            .values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        ),

        "department_chart": (
            Asset.objects
            .values("department__name")
            .annotate(total=Count("id"))
            .order_by("department__name")
        ),

        # --------------------------------------------------------
        # Warranty Alerts
        # --------------------------------------------------------

        "expiring_warranties": (
            Asset.objects.filter(
                warranty_expiry__isnull=False,
                warranty_expiry__lte=next_30_days,
                warranty_expiry__gte=today,
            ).order_by("warranty_expiry")
        ),
    }

    return render(
        request,
        "dashboard/index.html",
        context,
    )