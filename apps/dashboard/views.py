import csv
import logging
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import models
from django.db.models import Count, Max, Q, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from django.views.generic.edit import FormView
from django import forms

from apps.pages.models import ContactMessage, NewsletterSubscription, SiteText
from apps.properties.models import (
    BlockedPeriod,
    Booking,
    ICalSource,
    Property,
    PropertyImage,
)

logger = logging.getLogger(__name__)


class DashboardLoginRequiredMixin(LoginRequiredMixin):
    """Require login for all dashboard views."""

    login_url = reverse_lazy("dashboard:login")
    raise_exception = False


# ─── Dashboard Home ─────────────────────────────────────────────────


class DashboardHomeView(DashboardLoginRequiredMixin, TemplateView):
    """Dashboard home with stats cards, recent msgs, upcoming bookings."""

    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()

        # Stats cards
        ctx["unread_messages"] = ContactMessage.objects.filter(is_read=False).count()
        ctx["active_bookings"] = Booking.objects.filter(
            status="confirmed",
            check_out__gte=today,
        ).count()
        ctx["total_subscribers"] = NewsletterSubscription.objects.filter(
            is_active=True
        ).count()
        ctx["total_properties"] = Property.objects.filter(status="published").count()

        # Recent messages (last 5 unread first, then recent)
        recent_msgs = ContactMessage.objects.all().defer("message")[:5]
        ctx["recent_messages"] = recent_msgs

        # Upcoming bookings (next 5)
        ctx["upcoming_bookings"] = (
            Booking.objects.filter(status="confirmed", check_in__gte=today)
            .select_related("unit")
            .order_by("check_in")[:5]
        )

        # Quick stats for the current month
        month_start = today.replace(day=1)
        ctx["month_bookings"] = Booking.objects.filter(
            created_at__gte=month_start,
            status__in=["confirmed", "completed"],
        ).count()
        ctx["month_revenue"] = Booking.objects.filter(
            created_at__gte=month_start,
            status__in=["confirmed", "completed"],
        ).aggregate(total=Sum("total_price"))["total"] or Decimal("0")

        return ctx


# ─── Messages ───────────────────────────────────────────────────────


class MessageListView(DashboardLoginRequiredMixin, ListView):
    """List of contact messages."""

    model = ContactMessage
    template_name = "dashboard/messages_list.html"
    context_object_name = "messages"
    paginate_by = 20

    def get_queryset(self):
        qs = ContactMessage.objects.all().defer("message")
        status = self.request.GET.get("status")
        subject = self.request.GET.get("subject")
        if status == "unread":
            qs = qs.filter(is_read=False)
        elif status == "read":
            qs = qs.filter(is_read=True)
        if subject:
            qs = qs.filter(subject=subject)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["subject_choices"] = ContactMessage.SUBJECT_CHOICES
        ctx["current_status"] = self.request.GET.get("status", "")
        ctx["current_subject"] = self.request.GET.get("subject", "")
        ctx["unread_count"] = ContactMessage.objects.filter(is_read=False).count()
        return ctx


class MessageDetailView(DashboardLoginRequiredMixin, DetailView):
    """Show full message detail."""

    model = ContactMessage
    template_name = "dashboard/message_detail.html"
    context_object_name = "msg"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Auto-mark as read when viewing
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=["is_read"])
        return obj


class MessageToggleReadView(DashboardLoginRequiredMixin, View):
    """Toggle message read/unread status via POST."""

    def post(self, request, *args, **kwargs):
        msg = get_object_or_404(ContactMessage, pk=kwargs["pk"])
        msg.is_read = not msg.is_read
        msg.save(update_fields=["is_read"])
        status = "lue" if msg.is_read else "non lue"
        messages.success(request, f"Message marqué comme {status}.")
        return HttpResponseRedirect(reverse_lazy("dashboard:messages"))


# ─── Newsletter ────────────────────────────────────────────────────


class NewsletterListView(DashboardLoginRequiredMixin, ListView):
    """List of newsletter subscribers."""

    model = NewsletterSubscription
    template_name = "dashboard/newsletter_list.html"
    context_object_name = "subscribers"
    paginate_by = 50

    def get_queryset(self):
        qs = NewsletterSubscription.objects.all()
        status = self.request.GET.get("status")
        if status == "active":
            qs = qs.filter(is_active=True)
        elif status == "inactive":
            qs = qs.filter(is_active=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_status"] = self.request.GET.get("status", "")
        ctx["active_count"] = NewsletterSubscription.objects.filter(
            is_active=True
        ).count()
        return ctx


class NewsletterToggleView(DashboardLoginRequiredMixin, View):
    """Toggle subscriber active/inactive."""

    def post(self, request, *args, **kwargs):
        sub = get_object_or_404(NewsletterSubscription, pk=kwargs["pk"])
        sub.is_active = not sub.is_active
        sub.save(update_fields=["is_active"])
        status = "activé" if sub.is_active else "désactivé"
        messages.success(request, f"Abonné {status}.")
        return HttpResponseRedirect(reverse_lazy("dashboard:newsletter"))


class NewsletterExportView(DashboardLoginRequiredMixin, View):
    """Export subscribers to CSV."""

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = (
            f'attachment; filename="newsletter_{timezone.now().strftime("%Y%m%d")}.csv"'
        )
        response.write("\ufeff")  # BOM for Excel
        writer = csv.writer(response)
        writer.writerow(["Email", "Date d'inscription", "Actif"])
        for sub in NewsletterSubscription.objects.all().iterator():
            writer.writerow(
                [
                    sub.email,
                    sub.created_at.strftime("%Y-%m-%d %H:%M"),
                    "Oui" if sub.is_active else "Non",
                ]
            )
        return response


# ─── Bookings ───────────────────────────────────────────────────────


class BookingListView(DashboardLoginRequiredMixin, ListView):
    """List all bookings."""

    model = Booking
    template_name = "dashboard/bookings_list.html"
    context_object_name = "bookings"
    paginate_by = 20

    def get_queryset(self):
        qs = Booking.objects.all().select_related("unit")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_choices"] = Booking.STATUS_CHOICES
        ctx["current_status"] = self.request.GET.get("status", "")
        ctx["status_counts"] = {
            s: Booking.objects.filter(status=s).count()
            for s, _ in Booking.STATUS_CHOICES
        }
        return ctx


class BookingCreateView(DashboardLoginRequiredMixin, CreateView):
    """Create a new booking."""

    model = Booking
    template_name = "dashboard/booking_form.html"
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "unit",
        "check_in",
        "check_out",
        "guests",
        "total_price",
        "status",
        "source",
        "payment_status",
        "notes",
    ]
    success_url = reverse_lazy("dashboard:bookings")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouvelle réservation"
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Réservation créée avec succès.")
        return super().form_valid(form)


class BookingUpdateView(DashboardLoginRequiredMixin, UpdateView):
    """Edit an existing booking."""

    model = Booking
    template_name = "dashboard/booking_form.html"
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "unit",
        "check_in",
        "check_out",
        "guests",
        "total_price",
        "status",
        "source",
        "payment_status",
        "notes",
    ]
    success_url = reverse_lazy("dashboard:bookings")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Modifier la réservation"
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Réservation mise à jour.")
        return super().form_valid(form)


class BookingStatusUpdateView(DashboardLoginRequiredMixin, View):
    """Quick status change via POST."""

    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs["pk"])
        new_status = request.POST.get("status")
        if new_status and new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save(update_fields=["status"])
            messages.success(
                request,
                f"Réservation #{booking.pk} : statut mis à jour « {booking.get_status_display()} ».",
            )
        return HttpResponseRedirect(reverse_lazy("dashboard:bookings"))


class BookingCalendarView(DashboardLoginRequiredMixin, TemplateView):
    """Simple month-grid calendar showing bookings."""

    template_name = "dashboard/booking_calendar.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()

        year = int(self.request.GET.get("year", today.year))
        month = int(self.request.GET.get("month", today.month))

        import calendar as cal

        # Month navigation
        if month == 1:
            prev_month, prev_year = 12, year - 1
        else:
            prev_month, prev_year = month - 1, year
        if month == 12:
            next_month, next_year = 1, year + 1
        else:
            next_month, next_year = month + 1, year

        ctx["current_year"] = year
        ctx["current_month"] = month
        ctx["month_name"] = cal.month_name[month]
        ctx["prev_month"] = prev_month
        ctx["prev_year"] = prev_year
        ctx["next_month"] = next_month
        ctx["next_year"] = next_year

        # Build calendar grid
        cal_obj = cal.Calendar()
        weeks = []
        for week in cal_obj.monthdayscalendar(year, month):
            row = []
            for day in week:
                if day == 0:
                    row.append({"day": None, "bookings": [], "blocked": []})
                else:
                    d = date(year, month, day)
                    # Real bookings
                    day_bookings = list(
                        Booking.objects.filter(
                            Q(check_in__lte=d, check_out__gte=d),
                            status__in=["pending", "confirmed"],
                        ).select_related("unit")
                    )
                    # iCal-blocked periods (VEVENT DTEND is exclusive, so end_date > d)
                    day_blocked = list(
                        BlockedPeriod.objects.filter(
                            unit__status="published",
                            start_date__lte=d,
                            end_date__gt=d,
                        ).select_related("unit", "source")[:5]
                    )
                    row.append(
                        {
                            "day": day,
                            "bookings": day_bookings,
                            "blocked": day_blocked,
                            "is_today": d == today,
                        }
                    )
            weeks.append(row)

        ctx["weeks"] = weeks
        ctx["properties"] = Property.objects.filter(status="published")
        return ctx


# ─── Properties Stats ──────────────────────────────────────────────


class PropertyStatsView(DashboardLoginRequiredMixin, TemplateView):
    """Per-property booking and revenue stats."""

    template_name = "dashboard/properties_stats.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        properties = Property.objects.filter(status="published").annotate(
            total_bookings=Count("bookings"),
            confirmed_bookings=Count(
                "bookings", filter=Q(bookings__status="confirmed")
            ),
            total_revenue=Sum(
                "bookings__total_price",
                filter=Q(bookings__status__in=["confirmed", "completed"]),
            ),
        )
        ctx["properties"] = properties

        totals = Booking.objects.filter(
            status__in=["confirmed", "completed"]
        ).aggregate(
            total_bookings=Count("id"),
            total_revenue=Sum("total_price"),
        )
        ctx["totals"] = totals
        ctx["total_pending"] = Booking.objects.filter(status="pending").count()

        # iCal sources per property
        ctx["ical_sources"] = ICalSource.objects.filter(
            unit__status="published"
        ).select_related("unit")
        return ctx


# ─── iCal Management ──────────────────────────────────────────────


class ICalSourceForm(forms.ModelForm):
    class Meta:
        model = ICalSource
        fields = ["unit", "name", "url", "is_active"]
        widgets = {
            "url": forms.URLInput(attrs={"placeholder": "https://..."}),
        }


class ICalSourceCreateView(DashboardLoginRequiredMixin, FormView):
    """Add a new iCal source."""

    template_name = "dashboard/ical_source_form.html"
    form_class = ICalSourceForm
    success_url = reverse_lazy("dashboard:property_stats")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["section"] = "properties"
        ctx["title"] = "Ajouter une source iCal"
        return ctx

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Source iCal ajoutée.")
        return super().form_valid(form)


class ICalSourceDeleteView(DashboardLoginRequiredMixin, View):
    """Delete an iCal source."""

    def post(self, request, *args, **kwargs):
        source = get_object_or_404(ICalSource, pk=kwargs["pk"])
        source.blocked_periods.all().delete()
        source.delete()
        messages.success(request, "Source iCal supprimée.")
        return HttpResponseRedirect(reverse_lazy("dashboard:property_stats"))


class ICalSyncView(DashboardLoginRequiredMixin, View):
    """Trigger sync for a single iCal source."""

    def post(self, request, *args, **kwargs):
        from django.core.management import call_command
        from io import StringIO

        source_id = kwargs.get("pk")
        out = StringIO()
        call_command("sync_ical", source=source_id, clear=True, stdout=out)
        messages.success(request, out.getvalue())
        return HttpResponseRedirect(reverse_lazy("dashboard:property_stats"))


# ─── Property CRUD ──────────────────────────────────────────────────


LANGUAGES = [
    ("fr", "Français"),
    ("en", "English"),
    ("de", "Deutsch"),
    ("nl", "Nederlands"),
]

TRANSLATABLE_FIELDS = [
    "name",
    "subtitle",
    "summary",
    "description",
    "host_name",
    "house_rules",
    "check_in_time",
    "check_out_time",
    "distance_to_beach",
    "meta_title",
    "meta_description",
]


class PropertyListView(DashboardLoginRequiredMixin, ListView):
    """List all properties with full CRUD access."""

    model = Property
    template_name = "dashboard/property_list.html"
    context_object_name = "properties"
    paginate_by = 20

    def get_queryset(self):
        qs = Property.objects.all().prefetch_related("images")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["section"] = "properties"
        ctx["status_choices"] = Property.STATUS_CHOICES
        ctx["current_status"] = self.request.GET.get("status", "")
        return ctx


class PropertyFormMixin:
    """Shared logic between create and edit property views."""

    model = Property
    template_name = "dashboard/property_form.html"
    fields = [
        "name",
        "slug",
        "subtitle",
        "summary",
        "description",
        "status",
        "featured",
        "order",
        "city",
        "address",
        "latitude",
        "longitude",
        "distance_to_beach",
        "max_guests",
        "bedrooms",
        "beds",
        "bathrooms",
        "surface_area",
        "base_price",
        "cleaning_fee",
        "security_deposit",
        "currency",
        "amenities",
        "check_in_time",
        "check_out_time",
        "house_rules",
        "host_name",
        "registration_number",
        "meta_title",
        "meta_description",
    ]
    # translations is handled manually in the form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["section"] = "properties"
        ctx["languages"] = LANGUAGES
        ctx["translatable_fields"] = TRANSLATABLE_FIELDS
        if self.object:
            ctx["translations"] = self.object.translations or {}
        else:
            ctx["translations"] = {}
        return ctx

    def form_valid(self, form):
        # Merge translations from the POST data
        translations = {}
        for lang_code, _ in LANGUAGES:
            lang_data = {}
            for field in TRANSLATABLE_FIELDS:
                key = f"trans_{lang_code}_{field}"
                val = self.request.POST.get(key, "").strip()
                if val:
                    lang_data[field] = val
            if lang_data:
                translations[lang_code] = lang_data
        form.instance.translations = translations
        messages.success(self.request, "Propriété enregistrée.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard:property_edit", kwargs={"pk": self.object.pk})


class PropertyCreateView(DashboardLoginRequiredMixin, PropertyFormMixin, CreateView):
    """Create a new property."""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Nouvelle propriété"
        return ctx


class PropertyUpdateView(DashboardLoginRequiredMixin, PropertyFormMixin, UpdateView):
    """Edit an existing property."""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = f"Modifier — {self.object.name}"
        return ctx


class PropertyDeleteView(DashboardLoginRequiredMixin, View):
    """Delete a property via POST."""

    def post(self, request, *args, **kwargs):
        prop = get_object_or_404(Property, pk=kwargs["pk"])
        name = prop.name
        prop.delete()
        messages.success(request, f"Propriété « {name} » supprimée.")
        return HttpResponseRedirect(reverse_lazy("dashboard:property_list"))


class PropertyDetailView(DashboardLoginRequiredMixin, DetailView):
    """View a single property's details and manage its images."""

    model = Property
    template_name = "dashboard/property_detail.html"
    context_object_name = "prop"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["section"] = "properties"
        ctx["images"] = self.object.images.all().order_by("order")
        ctx["languages"] = LANGUAGES
        ctx["translations"] = self.object.translations or {}
        return ctx


# ─── Image Management ──────────────────────────────────────────────


class ImageUploadView(DashboardLoginRequiredMixin, View):
    """Upload one or more images for a property via POST."""

    def post(self, request, *args, **kwargs):
        prop = get_object_or_404(Property, pk=kwargs["pk"])
        files = request.FILES.getlist("images")
        if not files:
            messages.warning(request, "Aucune image sélectionnée.")
            return HttpResponseRedirect(
                reverse_lazy("dashboard:property_detail", kwargs={"pk": prop.pk})
            )

        max_order = (
            PropertyImage.objects.filter(property=prop).aggregate(
                max_order=models.Max("order")
            )["max_order"]
            or 0
        )

        for i, f in enumerate(files):
            PropertyImage.objects.create(
                property=prop,
                image=f,
                alt_text=request.POST.get("alt_text", ""),
                is_primary=False,
                order=max_order + i + 1,
            )

        # If first image, make it primary
        if not PropertyImage.objects.filter(property=prop, is_primary=True).exists():
            first = PropertyImage.objects.filter(property=prop).first()
            if first:
                first.is_primary = True
                first.save(update_fields=["is_primary"])

        count = len(files)
        messages.success(
            request,
            f"{count} image{'s' if count > 1 else ''} importée{'s' if count > 1 else ''}.",
        )
        return HttpResponseRedirect(
            reverse_lazy("dashboard:property_detail", kwargs={"pk": prop.pk})
        )


class ImageDeleteView(DashboardLoginRequiredMixin, View):
    """Delete a single image via POST."""

    def post(self, request, *args, **kwargs):
        img = get_object_or_404(PropertyImage, pk=kwargs["pk"])
        prop_pk = img.property.pk
        img.delete()
        messages.success(request, "Image supprimée.")
        return HttpResponseRedirect(
            reverse_lazy("dashboard:property_detail", kwargs={"pk": prop_pk})
        )


class ImageSetPrimaryView(DashboardLoginRequiredMixin, View):
    """Set an image as the primary one via POST."""

    def post(self, request, *args, **kwargs):
        img = get_object_or_404(PropertyImage, pk=kwargs["pk"])
        prop = img.property
        # Unset all others
        PropertyImage.objects.filter(property=prop, is_primary=True).update(
            is_primary=False
        )
        img.is_primary = True
        img.save(update_fields=["is_primary"])
        messages.success(request, "Image principale mise à jour.")
        return HttpResponseRedirect(
            reverse_lazy("dashboard:property_detail", kwargs={"pk": prop.pk})
        )


class ImageReorderView(DashboardLoginRequiredMixin, View):
    """Reorder images based on a comma-separated list of image PKs via POST."""

    def post(self, request, *args, **kwargs):
        prop = get_object_or_404(Property, pk=kwargs["pk"])
        order = request.POST.get("order", "")
        for i, img_pk in enumerate(order.split(",")):
            img_pk = img_pk.strip()
            if img_pk:
                PropertyImage.objects.filter(pk=img_pk, property=prop).update(order=i)
        messages.success(request, "Ordre des images mis à jour.")
        return HttpResponseRedirect(
            reverse_lazy("dashboard:property_detail", kwargs={"pk": prop.pk})
        )


# ─── SiteText Management ──────────────────────────────────────────


class SiteTextListView(DashboardLoginRequiredMixin, ListView):
    """List all site texts."""

    model = SiteText
    template_name = "dashboard/sitetext_list.html"
    context_object_name = "texts"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["section"] = "sitetext"
        return ctx


class SiteTextUpdateView(DashboardLoginRequiredMixin, UpdateView):
    """Edit a site text with language tabs."""

    model = SiteText
    template_name = "dashboard/sitetext_form.html"
    fields = ["key", "label"]  # translations handled manually

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["section"] = "sitetext"
        ctx["languages"] = LANGUAGES
        ctx["title"] = f"Modifier — {self.object.label or self.object.key}"
        return ctx

    def form_valid(self, form):
        translations = {}
        for lang_code, _ in LANGUAGES:
            val = self.request.POST.get(f"trans_{lang_code}", "").strip()
            if val:
                translations[lang_code] = val
        form.instance.translations = translations
        messages.success(self.request, "Texte enregistré.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard:sitetext_list")
