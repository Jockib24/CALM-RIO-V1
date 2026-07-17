import json
from datetime import datetime

from django.conf import settings

from .seo import local_business_structured_data


def site_settings(request):
    """Provide site-wide context to all templates.

    Includes site settings, SEO defaults, and JSON-LD structured data.
    """
    site = {
        "site_name": getattr(settings, "SITE_NAME", "CalmRio"),
        "site_description": getattr(settings, "SITE_DESCRIPTION", ""),
        "contact_email": getattr(settings, "CONTACT_EMAIL", ""),
        "contact_phone": getattr(settings, "CONTACT_PHONE", ""),
        "current_year": datetime.now().year,
    }

    # Build page-specific context
    path = request.path_info

    # Default OG image (overridable per template)
    og_image = request.build_absolute_uri(
        "/static/images/og-image.jpg"
    )

    # Breadcrumbs — set based on URL pattern
    breadcrumbs = None
    structured_data = []

    # Homepage
    if path == "/":
        breadcrumbs = None  # No breadcrumbs on homepage
        structured_data.append(local_business_structured_data(request))

    # About page
    elif "about" in path:
        breadcrumbs = [
            ("Accueil", "/"),
            ("À propos", request.path_info),
        ]

    # Contact page
    elif "contact" in path:
        breadcrumbs = [
            ("Accueil", "/"),
            ("Contact", request.path_info),
        ]

    # FAQ page
    elif "faq" in path:
        breadcrumbs = [
            ("Accueil", "/"),
            ("FAQ", request.path_info),
        ]

    # Local guide
    elif "local-guide" in path:
        breadcrumbs = [
            ("Accueil", "/"),
            ("Guide Local", request.path_info),
        ]

    # Properties
    elif "royan-appartement" in path:
        breadcrumbs = [
            ("Accueil", "/"),
            ("Royan — Appartement", request.path_info),
        ]
    elif "saint-trojan-villa" in path:
        breadcrumbs = [
            ("Accueil", "/"),
            ("Saint-Trojan — Villa", request.path_info),
        ]
    elif "saint-trojan-maison" in path:
        breadcrumbs = [
            ("Accueil", "/"),
            ("Saint-Trojan — Maison", request.path_info),
        ]

    # Legal
    elif "mentions-legales" in path:
        breadcrumbs = [
            ("Accueil", "/"),
            ("Mentions légales", request.path_info),
        ]
    elif "politique-de-confidentialite" in path:
        breadcrumbs = [
            ("Accueil", "/"),
            ("Politique de confidentialité", request.path_info),
        ]

    # Serialize JSON-LD
    if breadcrumbs:
        from .seo import breadcrumb_structured_data
        structured_data.append(
            breadcrumb_structured_data(request, breadcrumbs)
        )

    return {
        **site,
        "og_image_default": og_image,
        "structured_data": structured_data,
        "structured_data_json": json.dumps(structured_data, ensure_ascii=False)
        if structured_data
        else "",
    }
