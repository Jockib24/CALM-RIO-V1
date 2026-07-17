"""
SEO utilities for CalmRio.

Provides structured data builders and SEO helpers
used by the context processor and templates.
"""

import json


def local_business_structured_data(request):
    """JSON-LD for LocalBusiness schema.org markup."""
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "CalmRio",
        "description": "Locations de vacances premium à Royan et sur l'île d'Oléron",
        "url": request.build_absolute_uri("/"),
        "telephone": "+33600000000",
        "email": "contact@calm-rio.com",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Royan",
            "addressRegion": "Nouvelle-Aquitaine",
            "addressCountry": "FR",
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.95",
            "reviewCount": 42,
            "bestRating": "5",
        },
        "image": request.build_absolute_uri(
            "/static/images/og-image.jpg"
        ),
        "priceRange": "130€ - 200€/nuit",
        "areaServed": ["Royan", "Île d'Oléron", "Saint-Trojan-les-Bains"],
    }


def vacation_rental_structured_data(request, property_obj=None):
    """JSON-LD for VacationRental (individual property)."""
    if property_obj is None:
        return None

    return {
        "@context": "https://schema.org",
        "@type": "VacationRental",
        "name": property_obj.name,
        "description": property_obj.summary,
        "url": request.build_absolute_uri(property_obj.get_absolute_url()),
        "numberOfBedrooms": property_obj.bedrooms,
        "numberOfBathroomsTotal": property_obj.bathrooms,
        "maximumGuests": property_obj.max_guests,
        "priceRange": f"{property_obj.base_price}{property_obj.currency}/nuit",
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": amenity.name}
            for amenity in property_obj.amenities.all()
        ],
    }


def breadcrumb_structured_data(request, items):
    """JSON-LD for BreadcrumbList.

    items is a list of (name, url) tuples.
    """
    crumbs = []
    for i, (name, url) in enumerate(items, start=1):
        crumbs.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": request.build_absolute_uri(url),
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": crumbs,
    }
