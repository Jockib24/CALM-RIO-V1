import json

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            from apps.properties.models import Property

            props = Property.objects.filter(status="published").order_by("order")[:6]
            context["featured_properties"] = props

            # Build WebSite + ItemList schema
            site_url = "https://www.calm-rio.com"
            item_list = []
            for p in props:
                img = p.images.filter(is_primary=True).first()
                img_url = (
                    img.image.url
                    if img
                    else f"{site_url}/static/images/properties/{p.slug}/01.jpg"
                )
                item_list.append(
                    {
                        "@type": "VacationRental",
                        "url": f"{site_url}/{p.slug}/",
                        "name": p.name,
                        "image": img_url,
                        "description": p.summary[:300] if p.summary else "",
                    }
                )

            schema = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "WebSite",
                        "@id": f"{site_url}/#website",
                        "url": site_url,
                        "name": "CalmRio — Locations de vacances premium",
                        "description": "Locations de vacances premium à Royan et sur l'île d'Oléron.",
                        "inLanguage": "fr-FR",
                    },
                    {
                        "@type": "ItemList",
                        "@id": f"{site_url}/#properties",
                        "name": "Nos locations",
                        "itemListElement": [
                            {"@type": "ListItem", "position": i + 1, "item": it}
                            for i, it in enumerate(item_list)
                        ],
                    },
                ],
            }
            context["home_schema_ld"] = json.dumps(schema, indent=2)
        except Exception as e:
            context["featured_properties"] = []
            context["home_schema_ld"] = ""
        return context
