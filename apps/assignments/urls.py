from django.urls import path

from . import views

urlpatterns = [

    path(

        "checkout/<int:pk>/",

        views.checkout_asset,

        name="checkout_asset",

    ),

    path(
        "return/<int:pk>/",
        views.return_asset,
        name="return_asset",
    ),

]