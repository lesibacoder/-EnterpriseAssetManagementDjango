from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.department_index,
        name="department_index",
    ),

    path(
        "create/",
        views.department_create,
        name="department_create",
    ),

    path(
        "<int:pk>/",
        views.department_detail,
        name="department_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.department_update,
        name="department_update",
    ),

    path(
        "<int:pk>/delete/",
        views.department_delete,
        name="department_delete",
    ),

    path(
        "bulk-delete/",
        views.department_bulk_delete,
        name="department_bulk_delete",
    ),

]