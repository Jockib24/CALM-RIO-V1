from django.test import TestCase
from django.urls import reverse

from apps.properties.models import Property


def _create_property(slug, name=None, **kwargs):
    """Helper to create a Property with the given slug and defaults."""
    defaults = dict(
        name=name or slug.replace("-", " ").title(),
        summary=f"Summary for {slug}",
        description=f"Description for {slug}",
        status="published",
        base_price=100,
        city="Royan",
        max_guests=4,
        bedrooms=2,
        bathrooms=1,
    )
    defaults.update(kwargs)
    return Property.objects.create(slug=slug, **defaults)


class PropertyListViewTest(TestCase):
    def setUp(self):
        # Static views require matching Property in DB with slug
        self.published = _create_property("royan-appartement")

    def test_list_view_status_code(self):
        response = self.client.get(reverse("properties:royan_appartement"))
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        response = self.client.get(reverse("properties:royan_appartement"))
        self.assertTemplateUsed(response, "properties/royan-appartement.html")

    def test_detail_view_404_for_nonexistent(self):
        response = self.client.get("/nonexistent-property/")
        self.assertEqual(response.status_code, 404)


class PropertyDetailViewTest(TestCase):
    def setUp(self):
        self.apt = _create_property("royan-appartement", name="Royan Appartement")
        _create_property("saint-trojan-villa", name="Saint Trojan Villa")
        _create_property("saint-trojan-maison", name="Saint Trojan Maison")

    def test_static_property_view(self):
        response = self.client.get(reverse("properties:royan_appartement"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Royan")

    def test_static_property_view_context(self):
        response = self.client.get(reverse("properties:royan_appartement"))
        # The static views add booked_dates_json to context
        if hasattr(response.context, "get"):
            self.assertIn("booked_dates_json", response.context)

    def test_saint_trojan_villa_view(self):
        response = self.client.get(reverse("properties:saint_trojan_villa"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "properties/saint-trojan-villa.html")

    def test_saint_trojan_maison_view(self):
        response = self.client.get(reverse("properties:saint_trojan_maison"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "properties/saint-trojan-maison.html")
