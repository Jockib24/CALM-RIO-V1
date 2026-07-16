from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add featured properties once DB is populated
        try:
            from apps.properties.models import Property

            context["featured_properties"] = Property.objects.filter(
                status="published", featured=True
            ).order_by("order")[:6]
        except Exception:
            context["featured_properties"] = []
        return context
