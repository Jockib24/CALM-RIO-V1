from django.db import migrations


def add_test_ical_source(apps, schema_editor):
    ICalSource = apps.get_model("properties", "ICalSource")
    Property = apps.get_model("properties", "Property")

    try:
        appart = Property.objects.get(slug="royan-appartement")
        ICalSource.objects.update_or_create(
            unit=appart,
            name="Airbnb (test)",
            defaults={
                "url": "https://www.airbnb.fr/calendar/ical/1482761729141488146.ics?t=03ba7e5a850942f9b8932f6f68dd26ee",
                "is_active": True,
            },
        )
    except Property.DoesNotExist:
        pass  # Property not yet populated — run populate_properties first


def remove_test_ical_source(apps, schema_editor):
    ICalSource = apps.get_model("properties", "ICalSource")
    ICalSource.objects.filter(name="Airbnb (test)").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0004_property_translations"),
    ]

    operations = [
        migrations.RunPython(add_test_ical_source, remove_test_ical_source),
    ]
