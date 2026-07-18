import json
from datetime import datetime

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .seo import local_business_structured_data


def locale_info(request):
    """Provide locale metadata and direct language-switch URLs."""
    lang_to_locale = {
        "fr": "fr_FR",
        "en": "en_US",
        "es": "es_ES",
        "nl": "nl_NL",
    }
    flags = {
        "fr": "🇫🇷",
        "en": "🇬🇧",
        "es": "🇪🇸",
        "nl": "🇳🇱",
    }
    current_lang = getattr(request, "LANGUAGE_CODE", "fr")
    current_path = request.path_info or "/"

    # i18n_patterns uses prefix_default_language=False:
    #   French: /about/
    #   Other languages: /en/about/, /es/about/, /nl/about/
    path_without_language = current_path
    for code, _name in settings.LANGUAGES:
        prefix = f"/{code}/"
        if path_without_language == f"/{code}":
            path_without_language = "/"
            break
        if path_without_language.startswith(prefix):
            path_without_language = "/" + path_without_language[len(prefix):]
            break

    query_string = request.META.get("QUERY_STRING", "")
    query_suffix = f"?{query_string}" if query_string else ""
    language_switcher = []
    for code, name in settings.LANGUAGES:
        if code == settings.LANGUAGE_CODE:
            url = path_without_language
        else:
            clean_path = path_without_language.lstrip("/")
            url = f"/{code}/{clean_path}"
        if not url.endswith("/") and "." not in url.rsplit("/", 1)[-1]:
            url = f"{url}/"
        language_switcher.append(
            {
                "code": code,
                "name": name,
                "flag": flags.get(code, ""),
                "url": f"{url}{query_suffix}",
                "current": code == current_lang,
            }
        )

    return {
        "og_locale": lang_to_locale.get(current_lang, "fr_FR"),
        "html_lang": current_lang,
        "current_language_code": current_lang,
        "current_language_flag": flags.get(current_lang, ""),
        "language_switcher": language_switcher,
    }


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
    og_image = request.build_absolute_uri("/static/images/og-image.jpg")

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
            (_("Accueil"), "/"),
            (_("À propos"), request.path_info),
        ]

    # Contact page
    elif "contact" in path:
        breadcrumbs = [
            (_("Accueil"), "/"),
            (_("Contact"), request.path_info),
        ]

    # FAQ page
    elif "faq" in path:
        breadcrumbs = [
            (_("Accueil"), "/"),
            (_("FAQ"), request.path_info),
        ]

    # Local guide
    elif "local-guide" in path:
        breadcrumbs = [
            (_("Accueil"), "/"),
            (_("Guide Local"), request.path_info),
        ]

    # Properties
    elif "royan-appartement" in path:
        breadcrumbs = [
            (_("Accueil"), "/"),
            (_("Royan — Appartement"), request.path_info),
        ]
    elif "saint-trojan-villa" in path:
        breadcrumbs = [
            (_("Accueil"), "/"),
            (_("Saint-Trojan — Villa"), request.path_info),
        ]
    elif "saint-trojan-maison" in path:
        breadcrumbs = [
            (_("Accueil"), "/"),
            (_("Saint-Trojan — Maison"), request.path_info),
        ]

    # Legal
    elif "mentions-legales" in path:
        breadcrumbs = [
            (_("Accueil"), "/"),
            (_("Mentions légales"), request.path_info),
        ]
    elif "politique-de-confidentialite" in path:
        breadcrumbs = [
            (_("Accueil"), "/"),
            (_("Politique de confidentialité"), request.path_info),
        ]

    # Serialize JSON-LD
    if breadcrumbs:
        from django.utils.encoding import force_str
        from .seo import breadcrumb_structured_data

        # Convert lazy translation proxies to strings for JSON serialization
        breadcrumbs = [(force_str(label), url) for label, url in breadcrumbs]
        structured_data.append(breadcrumb_structured_data(request, breadcrumbs))

    return {
        **site,
        "og_image_default": og_image,
        "structured_data": structured_data,
        "structured_data_json": json.dumps(structured_data, ensure_ascii=False)
        if structured_data
        else "",
    }
