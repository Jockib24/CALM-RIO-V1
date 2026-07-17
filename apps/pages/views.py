import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.base import View

logger = logging.getLogger(__name__)

from .forms import ContactForm, NewsletterForm


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("pages:contact")

    def form_valid(self, form):
        # Save the message to the database
        from .models import ContactMessage

        contact = ContactMessage.objects.create(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data.get("last_name", ""),
            email=form.cleaned_data["email"],
            phone=form.cleaned_data.get("phone", ""),
            subject=form.cleaned_data["subject"],
            property_interest=form.cleaned_data.get("property_interest", ""),
            message=form.cleaned_data["message"],
            terms_accepted=form.cleaned_data.get("accept_terms", False),
        )

        # Send email notification to site admin
        try:
            send_mail(
                subject=f"CalmRio — Nouveau message: {contact.get_subject_display()}",
                message=(
                    f"De: {contact.first_name} {contact.last_name}\n"
                    f"Email: {contact.email}\n"
                    f"Téléphone: {contact.phone}\n"
                    f"Sujet: {contact.get_subject_display()}\n"
                    f"Logement: {contact.property_interest}\n\n"
                    f"Message:\n{contact.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            logger.warning("Failed to send contact notification email: %s", e)

        messages.success(
            self.request,
            "Merci pour votre message ! Nous vous répondrons dans les plus brefs délais.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Une erreur est survenue. Veuillez vérifier les champs ci-dessous.",
        )
        return super().form_invalid(form)


class FaqView(TemplateView):
    template_name = "pages/faq.html"


class LocalGuideView(TemplateView):
    template_name = "pages/local-guide.html"


class MentionsView(TemplateView):
    template_name = "pages/mentions-legales.html"


class PrivacyView(TemplateView):
    template_name = "pages/politique-de-confidentialite.html"


class NewsletterView(FormView):
    """Handle newsletter subscription."""

    form_class = NewsletterForm
    success_url = reverse_lazy("home:index")

    def form_valid(self, form):
        from .models import NewsletterSubscription

        NewsletterSubscription.objects.get_or_create(
            email=form.cleaned_data["email"]
        )
        messages.success(
            self.request,
            "Merci pour votre inscription à la newsletter !",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Email invalide. Veuillez réessayer.",
        )
        return super().form_invalid(form)


class RobotsView(View):
    """Generate robots.txt."""

    def get(self, request, *args, **kwargs):
        lines = [
            "User-agent: *",
            f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
            "Disallow: /admin/",
            "Allow: /",
        ]
        return HttpResponse(
            "\n".join(lines), content_type="text/plain"
        )


class SitemapView(View):
    """Generate XML sitemap."""

    def get(self, request, *args, **kwargs):
        pages = [
            ("home:index", "1.00", "daily"),
            ("pages:about", "0.80", "monthly"),
            ("pages:contact", "0.70", "monthly"),
            ("pages:faq", "0.70", "monthly"),
            ("pages:local_guide", "0.80", "weekly"),
            ("pages:mentions", "0.30", "yearly"),
            ("pages:privacy", "0.30", "yearly"),
            ("properties:royan_appartement", "0.90", "weekly"),
            ("properties:saint_trojan_villa", "0.90", "weekly"),
            ("properties:saint_trojan_maison", "0.90", "weekly"),
        ]
        urls_xml = ""
        for view_name, priority, changefreq in pages:
            try:
                url = request.build_absolute_uri(reverse(view_name))
                urls_xml += f"""
  <url>
    <loc>{url}</loc>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
            except Exception as e:
                logger.warning("Sitemap URL skipped for %%s: %%s", view_name, e)

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_xml}
</urlset>"""
        return HttpResponse(xml, content_type="application/xml")
