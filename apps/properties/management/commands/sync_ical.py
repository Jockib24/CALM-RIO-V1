"""
Synchronise les calendriers iCal (Airbnb, Booking.com, etc.) et crée les
périodes bloquées correspondantes.

Usage:
    python manage.py sync_ical
    python manage.py sync_ical --property=1
    python manage.py sync_ical --source=3
"""

import logging
from datetime import datetime, date

import requests
from icalendar import Calendar
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.properties.models import BlockedPeriod, ICalSource

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sync iCal sources and create blocked periods"

    def add_arguments(self, parser):
        parser.add_argument(
            "--property",
            type=int,
            help="Sync only for a specific property ID",
        )
        parser.add_argument(
            "--source",
            type=int,
            help="Sync only for a specific iCal source ID",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing blocked periods before syncing",
        )

    def handle(self, *args, **options):
        sources = ICalSource.objects.filter(is_active=True)

        if options["property"]:
            sources = sources.filter(unit_id=options["property"])
        if options["source"]:
            sources = sources.filter(pk=options["source"])

        if options["clear"]:
            cleared = BlockedPeriod.objects.filter(source__in=sources).count()
            BlockedPeriod.objects.filter(source__in=sources).delete()
            self.stdout.write(f"Supprimé {cleared} période(s) bloquée(s) existante(s).")

        total_new = 0
        for source in sources:
            self.stdout.write(
                f"Sync {source.name} — {source.unit.name} ...", ending=" "
            )
            try:
                count = self._sync_source(source)
                total_new += count
                source.last_synced = timezone.now()
                source.save(update_fields=["last_synced"])
                self.stdout.write(self.style.SUCCESS(f"{count} période(s)"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"ERREUR: {e}"))

        self.stdout.write(
            self.style.SUCCESS(f"\nSynchro terminée — {total_new} période(s) créée(s).")
        )

    def _sync_source(self, source):
        """Fetch and parse an iCal URL, store blocked periods."""
        resp = requests.get(
            source.url,
            timeout=30,
            headers={"User-Agent": "CalmRio/1.0 (iCal Sync)"},
        )
        resp.raise_for_status()

        cal = Calendar.from_ical(resp.text)
        new_count = 0

        for component in cal.walk():
            if component.name != "VEVENT":
                continue

            uid = str(component.get("UID", ""))
            dtstart = component.get("DTSTART").dt
            dtend = component.get("DTEND").dt
            summary = str(component.get("SUMMARY", ""))

            # Handle floating vs timezoned datetimes
            if hasattr(dtstart, "date"):
                start = dtstart.date()
            else:
                start = dtstart

            if hasattr(dtend, "date"):
                end = dtend.date()
            else:
                end = dtend

            # iCal DTEND is exclusive — adjust to inclusive
            # If end == start, it's a single-day event
            # If end > start, the effective end is end - 1 day for display
            # But we store as-is (exclusive end) to match iCal semantics

            # Avoid duplicates (same external_id + source)
            if (
                uid
                and BlockedPeriod.objects.filter(
                    source=source, external_id=uid
                ).exists()
            ):
                continue

            BlockedPeriod.objects.create(
                source=source,
                unit=source.unit,
                start_date=start,
                end_date=end,
                external_id=uid,
                summary=summary,
            )
            new_count += 1

        return new_count
