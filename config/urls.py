from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.properties.sitemaps import StaticViewSitemap, PropertySitemap, PageSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "properties": PropertySitemap,
    "pages": PageSitemap,
}

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Dashboard (outside i18n_patterns — language-independent)
    path("dashboard/", include("apps.dashboard.urls")),
    # Language switcher (outside i18n_patterns)
    path("i18n/", include("django.conf.urls.i18n")),
    # Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps, "template_name": "sitemap.xml"},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

# i18n-prefixed URLs (fr=default, no prefix)
urlpatterns += i18n_patterns(
    # Home
    path("", include("apps.home.urls")),
    # Pages
    path("", include("apps.pages.urls")),
    # Properties
    path("", include("apps.properties.urls")),
    prefix_default_language=False,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
