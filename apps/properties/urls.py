from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    # Legacy static template views (working now, DB not yet populated)
    path(
        "royan-appartement/",
        views.RoyanAppartementView.as_view(),
        name="royan_appartement",
    ),
    path(
        "saint-trojan-villa/",
        views.SaintTrojanVillaView.as_view(),
        name="saint_trojan_villa",
    ),
    path(
        "saint-trojan-maison/",
        views.SaintTrojanMaisonView.as_view(),
        name="saint_trojan_maison",
    ),
    # Public booking request
    path(
        "reserver/",
        views.BookingRequestView.as_view(),
        name="booking_request",
    ),
    # Database-backed views (enable once DB is populated via admin)
    # path("", views.PropertyListView.as_view(), name="list"),
    # path("<slug:slug>/", views.PropertyDetailView.as_view(), name="detail"),
]
