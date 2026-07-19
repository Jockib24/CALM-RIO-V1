from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache


class SiteText(models.Model):
    """A site-wide translatable text snippet (hero title, section intro, etc.)."""

    key = models.SlugField(
        _("Clé"),
        max_length=100,
        unique=True,
        help_text="Identifiant unique (ex: 'hero_title', 'about_intro')",
    )
    label = models.CharField(
        _("Libellé"),
        max_length=200,
        help_text="Description lisible de ce champ dans l'admin",
    )
    translations = models.JSONField(
        _("Traductions"),
        default=dict,
        blank=True,
        help_text="Contenu multilingue — {'fr': 'Bonjour', 'en': 'Hello'}",
    )
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Texte du site")
        verbose_name_plural = _("Textes du site")
        ordering = ["key"]

    def __str__(self):
        return self.label or self.key

    def get_text(self, lang="fr"):
        """Get the text for a given language, fallback to first available."""
        if isinstance(self.translations, dict):
            val = self.translations.get(lang)
            if val:
                return val
            # fallback to any available translation
            for v in self.translations.values():
                if v:
                    return v
        return ""

    def save(self, *args, **kwargs):
        # Invalidate cache on save
        cache.delete(f"sitetext_{self.key}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete(f"sitetext_{self.key}")
        super().delete(*args, **kwargs)


class ContactMessage(models.Model):
    """Contact form submission."""

    SUBJECT_CHOICES = [
        ("reservation", _("Réservation")),
        ("information", _("Demande d'information")),
        ("disponibilite", _("Vérification de disponibilité")),
        ("tarif", _("Demande de tarif")),
        ("reclamation", _("Réclamation")),
        ("autre", _("Autre")),
    ]

    first_name = models.CharField(_("Prénom"), max_length=100)
    last_name = models.CharField(_("Nom"), max_length=100, blank=True)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Téléphone"), max_length=20, blank=True)
    subject = models.CharField(_("Sujet"), max_length=50, choices=SUBJECT_CHOICES)
    property_interest = models.CharField(
        _("Logement concerné"), max_length=50, blank=True
    )
    message = models.TextField(_("Message"))
    terms_accepted = models.BooleanField(_("CGV acceptées"), default=False)
    is_read = models.BooleanField(_("Lu"), default=False)
    created_at = models.DateTimeField(_("Reçu le"), auto_now_add=True)

    class Meta:
        verbose_name = _("Message de contact")
        verbose_name_plural = _("Messages de contact")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.get_subject_display()}"


class NewsletterSubscription(models.Model):
    """Newsletter email subscription."""

    email = models.EmailField(_("Email"), unique=True)
    is_active = models.BooleanField(_("Actif"), default=True)
    created_at = models.DateTimeField(_("Inscrit le"), auto_now_add=True)

    class Meta:
        verbose_name = _("Abonné newsletter")
        verbose_name_plural = _("Abonnés newsletter")
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class Page(models.Model):
    """Editable static page (About, Legal, Privacy, FAQ, Local Guide)."""

    TEMPLATE_CHOICES = [
        ("about", _("À propos")),
        ("contact", _("Contact")),
        ("faq", _("FAQ")),
        ("local_guide", _("Guide local")),
        ("legal", _("Mentions légales")),
        ("privacy", _("Politique de confidentialité")),
        ("custom", _("Personnalisée")),
    ]

    title = models.CharField(_("Titre"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    template = models.CharField(
        _("Template"),
        max_length=50,
        choices=TEMPLATE_CHOICES,
        default="custom",
        help_text=_("Sélectionnez le template à utiliser pour l'affichage"),
    )
    content = models.TextField(
        _("Contenu"),
        blank=True,
        help_text=_("Contenu de la page (HTML autorisé)"),
    )
    meta_title = models.CharField(
        _("Meta title"), max_length=70, blank=True, help_text=_("Titre SEO")
    )
    meta_description = models.CharField(
        _("Meta description"),
        max_length=160,
        blank=True,
        help_text=_("Description SEO"),
    )
    is_published = models.BooleanField(_("Publiée"), default=True)
    order = models.PositiveIntegerField(_("Ordre"), default=0)
    created_at = models.DateTimeField(_("Créée le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mise à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        if self.template == "about":
            return reverse("pages:about")
        elif self.template == "contact":
            return reverse("pages:contact")
        elif self.template == "faq":
            return reverse("pages:faq")
        elif self.template == "local_guide":
            return reverse("pages:local_guide")
        elif self.template == "legal":
            return reverse("pages:mentions")
        elif self.template == "privacy":
            return reverse("pages:privacy")
        return f"/{self.slug}/"
