from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.base import View

from .forms import ContactForm


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("pages:contact")

    def form_valid(self, form):
        # Save the message to the database
        from .models import ContactMessage

        ContactMessage.objects.create(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data.get("last_name", ""),
            email=form.cleaned_data["email"],
            phone=form.cleaned_data.get("phone", ""),
            subject=form.cleaned_data["subject"],
            property_interest=form.cleaned_data.get("property_interest", ""),
            message=form.cleaned_data["message"],
        )
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
            except Exception:
                pass

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_xml}
</urlset>"""
        return HttpResponse(xml, content_type="application/xml")
