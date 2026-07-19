import json
from datetime import date, timedelta

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView

from .models import Property, Booking, BlockedPeriod


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
        return context


class SaintTrojanVillaView(TemplateView):
    template_name = "properties/saint-trojan-villa.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_get_property_context("saint-trojan-villa"))
        return context


class SaintTrojanMaisonView(TemplateView):
    template_name = "properties/saint-trojan-maison.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_get_property_context("saint-trojan-maison"))
        return context
