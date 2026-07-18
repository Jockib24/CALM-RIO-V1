from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Language switcher (outside i18n_patterns)
    path("i18n/", include("django.conf.urls.i18n")),
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
