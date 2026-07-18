from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "dashboard"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="dashboard/login.html",
            next_page="dashboard:home",
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="dashboard:login"), name="logout"),
    path("", views.DashboardHomeView.as_view(), name="home"),
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
    path("properties/", views.PropertyStatsView.as_view(), name="properties"),
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
]
