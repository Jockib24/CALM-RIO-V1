import json
import logging
from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView, FormView

from .forms import BookingRequestForm
from .models import Property, Booking, BlockedPeriod

logger = logging.getLogger(__name__)


class PropertyListView(ListView):
    """List all published properties."""

    model = Property
    template_name = "properties/list.html"
    context_object_name = "properties"

    def get_queryset(self):
        return Property.objects.filter(status="published").order_by("order")


class PropertyDetailView(DetailView):
    """Display a single property by slug."""

    model = Property
    template_name = "properties/detail.html"
    context_object_name = "property"

    def get_queryset(self):
        return Property.objects.filter(status="published")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["primary_image"] = self.object.images.filter(is_primary=True).first()
        context["gallery_images"] = self.object.images.filter(
            is_primary=False
        ).order_by("order")
        return context


def _build_schema(prop):
    """Build Schema.org VacationRental JSON-LD dict for a property."""
    site_url = "https://www.calm-rio.com"
    prop_url = f"{site_url}/{prop.slug}/"

    images = []
    for img in prop.images.all()[:10]:
        images.append(img.image.url)
    if not images:
        images = [f"{site_url}/static/images/properties/{prop.slug}/01.jpg"]

    schema = {
        "@context": "https://schema.org",
        "@type": "VacationRental",
        "name": prop.name,
        "description": prop.description[:500] if prop.description else "",
        "url": prop_url,
        "image": images,
        "numberOfBedrooms": prop.bedrooms,
        "numberOfBathroomsTotal": prop.bathrooms,
        "occupancy": {"@type": "QuantitativeValue", "maxValue": prop.max_guests},
        "petsAllowed": "animaux" in prop.house_rules.lower()
        if prop.house_rules
        else False,
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": a.name}
            for a in prop.amenities.all()
        ],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": prop.city,
            "streetAddress": prop.address or prop.city,
            "addressCountry": "FR",
        },
        "offers": {
            "@type": "Offer",
            "price": str(prop.base_price),
            "priceCurrency": "EUR",
            "availability": "https://schema.org/InStock",
        },
    }
    if prop.latitude and prop.longitude:
        schema["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": prop.latitude,
            "longitude": prop.longitude,
        }
    return json.dumps(schema, indent=2)


def _get_property_context(slug):
    """Helper: gather property, images, and booked dates for a property."""
    prop = get_object_or_404(Property, slug=slug, status="published")
    primary = prop.images.filter(is_primary=True).first()
    gallery = prop.images.filter(is_primary=False).order_by("order")

    # Collect all booked/blocked date ranges
    today = date.today()
    end_date = today + timedelta(days=365)
    booked = []

    confirmed_bookings = Booking.objects.filter(
        unit=prop,
        status="confirmed",
        check_in__lt=end_date,
        check_out__gte=today,
    )
    for b in confirmed_bookings:
        booked.append({"start": b.check_in.isoformat(), "end": b.check_out.isoformat()})

    blocked = BlockedPeriod.objects.filter(
        unit=prop,
        start_date__lt=end_date,
        end_date__gte=today,
    )
    for bp in blocked:
        booked.append(
            {"start": bp.start_date.isoformat(), "end": bp.end_date.isoformat()}
        )

    return {
        "property": prop,
        "primary_image": primary,
        "gallery_images": gallery,
        "booked_dates": booked,
        "schema_ld": _build_schema(prop),
        "booked_dates_json": json.dumps(booked),
    }


# Legacy static template views (used until DB is populated)
class RoyanAppartementView(TemplateView):
    template_name = "properties/royan-appartement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_get_property_context("royan-appartement"))
        context["today"] = date.today()
        return context


class SaintTrojanVillaView(TemplateView):
    template_name = "properties/saint-trojan-villa.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_get_property_context("saint-trojan-villa"))
        context["today"] = date.today()
        return context


class SaintTrojanMaisonView(TemplateView):
    template_name = "properties/saint-trojan-maison.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_get_property_context("saint-trojan-maison"))
        context["today"] = date.today()
        return context


class BookingRequestView(FormView):
    """Handle public booking requests from property pages."""

    form_class = BookingRequestForm
    http_method_names = ["post"]

    def form_valid(self, form):
        slug = form.cleaned_data["property_slug"]
        prop = get_object_or_404(Property, slug=slug, status="published")

        # Calculate total price (approximate: base_price * nights)
        nights = (form.cleaned_data["check_out"] - form.cleaned_data["check_in"]).days
        total_price = prop.base_price * nights
        if prop.cleaning_fee:
            total_price += prop.cleaning_fee

        booking = Booking.objects.create(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data.get("last_name", ""),
            email=form.cleaned_data["email"],
            phone=form.cleaned_data.get("phone", ""),
            unit=prop,
            check_in=form.cleaned_data["check_in"],
            check_out=form.cleaned_data["check_out"],
            guests=form.cleaned_data["guests"],
            total_price=total_price,
            status="pending",
            source="direct",
            notes=form.cleaned_data.get("message", ""),
        )

        # Email notification to admin
        try:
            send_mail(
                subject=f"CalmRio — Nouvelle demande de réservation: {prop.name}",
                message=(
                    f"De: {booking.first_name} {booking.last_name}\n"
                    f"Email: {booking.email}\n"
                    f"Téléphone: {booking.phone}\n"
                    f"Logement: {prop.name}\n"
                    f"Arrivée: {booking.check_in}\n"
                    f"Départ: {booking.check_out}\n"
                    f"Voyageurs: {booking.guests}\n"
                    f"Total estimé: {total_price}€\n\n"
                    f"Message:\n{booking.notes}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            logger.warning("Failed to send booking notification email: %s", e)

        messages.success(
            self.request,
            "Merci pour votre demande de réservation ! Nous vous répondrons "
            "dans les plus brefs délais pour confirmer votre séjour.",
        )
        return redirect(prop.get_absolute_url())

    def form_invalid(self, form):
        # Extract the slug from the form to redirect back
        slug = form.data.get("property_slug", "")
        prop = get_object_or_404(Property, slug=slug, status="published")

        for error in form.non_field_errors():
            messages.error(self.request, error)
        for field, errors in form.errors.items():
            if field == "__all__":
                continue
            for error in errors:
                messages.error(self.request, f"{form.fields[field].label}: {error}")

        return redirect(prop.get_absolute_url())
