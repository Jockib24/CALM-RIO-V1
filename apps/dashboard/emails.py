"""Email utilities for the dashboard app."""

import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_booking_confirmation(booking):
    """Send a booking confirmation email to the guest."""
    if not booking.email:
        logger.warning("Booking #%s has no email — skipping confirmation.", booking.pk)
        return False

    subject = f"✅ Réservation confirmée — {booking.unit.name} — CalmRio"
    html_content = render_to_string(
        "dashboard/emails/booking_confirmation.html",
        {"booking": booking},
    )
    text_content = strip_tags(html_content)

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        logger.info("Confirmation email sent to %s for booking #%s", booking.email, booking.pk)
        return True
    except Exception as e:
        logger.error("Failed to send confirmation to %s: %s", booking.email, e)
        return False
