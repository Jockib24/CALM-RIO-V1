from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("faq/", views.FaqView.as_view(), name="faq"),
    path("local-guide/", views.LocalGuideView.as_view(), name="local_guide"),
    path("mentions-legales/", views.MentionsView.as_view(), name="mentions"),
    path(
        "politique-de-confidentialite/",
        views.PrivacyView.as_view(),
        name="privacy",
    ),
    # SEO
    path("sitemap.xml", views.SitemapView.as_view(), name="sitemap"),
    path("robots.txt", views.RobotsView.as_view(), name="robots"),
]
