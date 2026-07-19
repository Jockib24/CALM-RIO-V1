from django.test import TestCase
from django.urls import reverse

from apps.properties.models import Property


class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse("home:index"))
        self.assertTemplateUsed(response, "home/index.html")

    def test_home_view_contains_properties(self):
        Property.objects.create(
            name="Test Property",
            slug="test-property",
            summary="A test",
            description="Description",
            status="published",
            featured=True,
        )
        response = self.client.get(reverse("home:index"))
        self.assertContains(response, "Test Property")

    def test_home_view_no_properties(self):
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_schema(self):
        Property.objects.create(
            name="Schema Property",
            slug="schema-property",
            summary="Schema test",
            description="Schema description",
            status="published",
            featured=True,
        )
        response = self.client.get(reverse("home:index"))
        self.assertContains(response, "schema.org")
