from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.asset_list,
        name="asset_list",
    ),

    path(
        "<int:pk>/",
        views.detail,
        name="asset_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.edit,
        name="asset_edit",
    ),

]