from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from .models import Property


class PropertyListView(ListView):
    """List all published properties."""

    model = Property
    template_name = "properties/list.html"
    context_object_name = "properties"

    def get_queryset(self):
        return Property.objects.filter(status="published").order_by("order")


class PropertyDetailView(DetailView):
    """Display a single property by slug."""

    model = Property
    template_name = "properties/detail.html"
    context_object_name = "property"

    def get_queryset(self):
        return Property.objects.filter(status="published")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["primary_image"] = self.object.images.filter(
            is_primary=True
        ).first()
        context["gallery_images"] = self.object.images.filter(
            is_primary=False
        ).order_by("order")
        return context


# Legacy static template views (used until DB is populated)
class RoyanAppartementView(TemplateView):
    template_name = "properties/royan-appartement.html"


class SaintTrojanVillaView(TemplateView):
    template_name = "properties/saint-trojan-villa.html"


class SaintTrojanMaisonView(TemplateView):
    template_name = "properties/saint-trojan-maison.html"
