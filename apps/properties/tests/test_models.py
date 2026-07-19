from datetime import date, timedelta

from django.test import TestCase

from apps.properties.models import (
    Amenity,
    Property,
    PropertyImage,
    Booking,
    ICalSource,
    BlockedPeriod,
)


class AmenityModelTest(TestCase):
    def setUp(self):
        self.amenity = Amenity.objects.create(
            name="WiFi haut débit",
            icon="fas fa-wifi",
            order=1,
        )

    def test_amenity_creation(self):
        self.assertEqual(str(self.amenity), "WiFi haut débit")
        self.assertEqual(self.amenity.icon, "fas fa-wifi")
        self.assertEqual(self.amenity.order, 1)

    def test_amenity_ordering(self):
        Amenity.objects.create(name="Parking", order=2)
        Amenity.objects.create(name="Cuisine", order=3)
        qs = Amenity.objects.all()
        self.assertEqual(qs[0].name, "WiFi haut débit")


class PropertyModelTest(TestCase):
    def setUp(self):
        self.amenity = Amenity.objects.create(name="WiFi", icon="fas fa-wifi")
        self.property = Property.objects.create(
            name="Test Appartement",
            slug="test-appartement",
            subtitle="Royan, test",
            summary="Un appartement de test",
            description="Description détaillée de test",
            status="published",
            featured=True,
            city="Royan",
            max_guests=4,
            bedrooms=2,
            beds=2,
            bathrooms=1,
            base_price=130,
            surface_area="60 m²",
        )
        self.property.amenities.add(self.amenity)

    def test_property_creation(self):
        self.assertEqual(str(self.property), "Test Appartement")
        self.assertEqual(self.property.status, "published")
        self.assertTrue(self.property.featured)

    def test_property_slug_auto(self):
        p = Property(name="No Slug", summary="test", description="test")
        p.save()
        self.assertEqual(p.slug, "no-slug")

    def test_get_absolute_url(self):
        url = self.property.get_absolute_url()
        self.assertEqual(url, "/royan-appartement/")

    def test_property_default_status(self):
        p = Property(name="Draft", summary="draft", description="draft")
        p.save()
        self.assertEqual(p.status, "draft")

    def test_property_default_ordering(self):
        Property.objects.all().delete()
        Property.objects.create(name="Second", summary="2", description="2", order=2)
        Property.objects.create(name="First", summary="1", description="1", order=1)
        qs = Property.objects.all()
        self.assertEqual(qs[0].name, "First")
        self.assertEqual(qs[1].name, "Second")

    def test_property_amenities_relation(self):
        self.assertIn(self.amenity, self.property.amenities.all())
        self.assertEqual(self.property.amenities.count(), 1)

    def test_published_filter(self):
        Property.objects.create(
            name="Hidden", slug="hidden", summary="h", description="h", status="hidden"
        )
        published = Property.objects.filter(status="published")
        self.assertEqual(published.count(), 1)
        self.assertEqual(published.first().name, "Test Appartement")

    def test_featured_filter(self):
        Property.objects.create(
            name="Not Featured",
            slug="not-featured",
            summary="nf",
            description="nf",
            featured=False,
        )
        featured = Property.objects.filter(featured=True)
        self.assertEqual(featured.count(), 1)


class PropertyImageModelTest(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            name="Test",
            slug="test-img",
            summary="img",
            description="img",
        )

    def test_image_ordering(self):
        img1 = PropertyImage.objects.create(
            property=self.property, order=2, image="properties/test/img1.jpg"
        )
        img2 = PropertyImage.objects.create(
            property=self.property, order=1, image="properties/test/img2.jpg"
        )
        qs = PropertyImage.objects.all()
        self.assertEqual(qs[0], img2)
        self.assertEqual(qs[1], img1)

    def test_primary_image(self):
        img1 = PropertyImage.objects.create(
            property=self.property,
            is_primary=True,
            order=1,
            image="properties/test/primary.jpg",
        )
        PropertyImage.objects.create(
            property=self.property,
            is_primary=False,
            order=2,
            image="properties/test/secondary.jpg",
        )
        primary = PropertyImage.objects.filter(
            property=self.property, is_primary=True
        ).first()
        self.assertEqual(primary, img1)


class BookingModelTest(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            name="Test Booking",
            slug="test-booking",
            summary="booking",
            description="booking",
        )
        self.booking = Booking.objects.create(
            first_name="Jean",
            last_name="Dupont",
            email="jean@example.com",
            unit=self.property,
            check_in=date(2026, 8, 1),
            check_out=date(2026, 8, 5),
            guests=2,
            total_price=520,
            status="confirmed",
        )

    def test_booking_creation(self):
        expected = f"Jean Dupont — Test Booking (2026-08-01)"
        self.assertEqual(str(self.booking), expected)

    def test_nights_property(self):
        self.assertEqual(self.booking.nights, 4)

    def test_booking_status_choices(self):
        self.assertIn(self.booking.status, dict(Booking.STATUS_CHOICES))

    def test_booking_source_default(self):
        self.assertEqual(self.booking.source, "direct")

    def test_booking_payment_default(self):
        self.assertEqual(self.booking.payment_status, "unpaid")

    def test_pending_booking(self):
        Booking.objects.create(
            first_name="Marie",
            email="marie@example.com",
            unit=self.property,
            check_in=date(2026, 9, 1),
            check_out=date(2026, 9, 3),
            status="pending",
        )
        self.assertEqual(Booking.objects.filter(status="pending").count(), 1)


class ICalSourceModelTest(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            name="Test iCal",
            slug="test-ical",
            summary="ical",
            description="ical",
        )
        self.source = ICalSource.objects.create(
            unit=self.property,
            name="Airbnb",
            url="https://www.airbnb.com/calendar/ical/test.ics",
            is_active=True,
        )

    def test_ical_source_creation(self):
        self.assertEqual(str(self.source), "Airbnb — Test iCal")
        self.assertTrue(self.source.is_active)

    def test_ical_source_inactive(self):
        source2 = ICalSource.objects.create(
            unit=self.property,
            name="Booking.com",
            url="https://www.booking.com/ical/test.ics",
            is_active=False,
        )
        self.assertFalse(source2.is_active)


class BlockedPeriodModelTest(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            name="Test Blocked",
            slug="test-blocked",
            summary="blocked",
            description="blocked",
        )
        self.source = ICalSource.objects.create(
            unit=self.property,
            name="Airbnb",
            url="https://airbnb.com/ical/test.ics",
        )
        self.period = BlockedPeriod.objects.create(
            source=self.source,
            unit=self.property,
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 15),
            external_id="abc123",
            summary="Réservé",
        )

    def test_blocked_period_creation(self):
        expected = f"Test Blocked: 2026-08-10 → 2026-08-15"
        self.assertEqual(str(self.period), expected)

    def test_blocked_period_indexes(self):
        """Verify we can filter by unit and date range."""
        qs = BlockedPeriod.objects.filter(
            unit=self.property,
            start_date__gte=date(2026, 8, 1),
            end_date__lte=date(2026, 8, 31),
        )
        self.assertEqual(qs.count(), 1)
