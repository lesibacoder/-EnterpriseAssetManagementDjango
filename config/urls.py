from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # AssetFlow Application
    path(
        "",
        include("apps.dashboard.urls"),
    ),

    # Asset Management
    path(
        "assets/",
        include("apps.assets.urls"),
    ),

    # Assignments Management
    path(
        "assignments/",
        include("apps.assignments.urls"),
    ),

    # Employees Management
    path(
        "employees/",
        include("apps.employees.urls"),
    ),

    # Departments Management
    path(
        "departments/",
        include("apps.departments.urls"),
    ),

    # Django Admin
    path(
        "admin/",
        admin.site.urls,
    ),


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )