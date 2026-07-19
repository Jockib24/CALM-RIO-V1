from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "dashboard"

urlpatterns = [
    # Auth
    path(
        "login/",
        LoginView.as_view(
            template_name="dashboard/login.html",
            next_page="dashboard:home",
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="dashboard:login"), name="logout"),
    # Home
    path("", views.DashboardHomeView.as_view(), name="home"),
    # Messages
    path("messages/", views.MessageListView.as_view(), name="messages"),
    path(
        "messages/<int:pk>/",
        views.MessageDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "messages/<int:pk>/toggle-read/",
        views.MessageToggleReadView.as_view(),
        name="message_toggle_read",
    ),
    # Newsletter
    path("newsletter/", views.NewsletterListView.as_view(), name="newsletter"),
    path(
        "newsletter/<int:pk>/toggle/",
        views.NewsletterToggleView.as_view(),
        name="newsletter_toggle",
    ),
    path(
        "newsletter/export/",
        views.NewsletterExportView.as_view(),
        name="newsletter_export",
    ),
    # Bookings
    path("bookings/", views.BookingListView.as_view(), name="bookings"),
    path("bookings/new/", views.BookingCreateView.as_view(), name="booking_create"),
    path(
        "bookings/<int:pk>/edit/",
        views.BookingUpdateView.as_view(),
        name="booking_edit",
    ),
    path(
        "bookings/<int:pk>/status/",
        views.BookingStatusUpdateView.as_view(),
        name="booking_status",
    ),
    path(
        "bookings/calendar/",
        views.BookingCalendarView.as_view(),
        name="booking_calendar",
    ),
    # Properties — Full CRUD
    path("properties/", views.PropertyListView.as_view(), name="property_list"),
    path(
        "properties/stats/",
        views.PropertyStatsView.as_view(),
        name="property_stats",
    ),
    path(
        "properties/new/",
        views.PropertyCreateView.as_view(),
        name="property_create",
    ),
    path(
        "properties/<int:pk>/",
        views.PropertyDetailView.as_view(),
        name="property_detail",
    ),
    path(
        "properties/<int:pk>/edit/",
        views.PropertyUpdateView.as_view(),
        name="property_edit",
    ),
    path(
        "properties/<int:pk>/delete/",
        views.PropertyDeleteView.as_view(),
        name="property_delete",
    ),
    # Images
    path(
        "properties/<int:pk>/images/upload/",
        views.ImageUploadView.as_view(),
        name="image_upload",
    ),
    path(
        "images/<int:pk>/delete/",
        views.ImageDeleteView.as_view(),
        name="image_delete",
    ),
    path(
        "images/<int:pk>/set-primary/",
        views.ImageSetPrimaryView.as_view(),
        name="image_set_primary",
    ),
    path(
        "properties/<int:pk>/images/reorder/",
        views.ImageReorderView.as_view(),
        name="image_reorder",
    ),
    # iCal
    path(
        "properties/ical/add/",
        views.ICalSourceCreateView.as_view(),
        name="ical_add",
    ),
    path(
        "properties/ical/<int:pk>/delete/",
        views.ICalSourceDeleteView.as_view(),
        name="ical_delete",
    ),
    path(
        "properties/ical/<int:pk>/sync/",
        views.ICalSyncView.as_view(),
        name="ical_sync",
    ),
    # SiteTexts
    path("textes/", views.SiteTextListView.as_view(), name="sitetext_list"),
    path(
        "textes/<int:pk>/edit/",
        views.SiteTextUpdateView.as_view(),
        name="sitetext_edit",
    ),
]
