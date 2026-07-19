from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.properties.models import Property
from apps.pages.models import Page


class StaticViewSitemap(Sitemap):
    """Static pages sitemap — multi-language with hreflang alternates."""

    priority = 0.8
    changefreq = "weekly"
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return [
            "home:index",
            "pages:local_guide",
            "pages:about",
            "pages:contact",
            "pages:faq",
            "pages:mentions",
            "pages:privacy",
        ]

    def location(self, item):
        return reverse(item)


class PropertySitemap(Sitemap):
    """Property pages sitemap — French only, no alternates."""

    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Property.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        # Map slugs to legacy URL names
        slug_to_url = {
            "royan-appartement": "properties:royan_appartement",
            "saint-trojan-villa": "properties:saint_trojan_villa",
            "saint-trojan-maison": "properties:saint_trojan_maison",
        }
        url_name = slug_to_url.get(item.slug)
        if url_name:
            return reverse(url_name)
        # Fallback to detail view if it exists
        try:
            return reverse("properties:detail", kwargs={"slug": item.slug})
        except Exception:
            return f"/{item.slug}/"


class PageSitemap(Sitemap):
    """CMS pages sitemap."""

    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return Page.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
