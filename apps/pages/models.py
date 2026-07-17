from django.db import models


class ContactMessage(models.Model):
    """Contact form submission."""

    SUBJECT_CHOICES = [
        ("reservation", "Réservation"),
        ("information", "Demande d'information"),
        ("disponibilite", "Vérification de disponibilité"),
        ("tarif", "Demande de tarif"),
        ("reclamation", "Réclamation"),
        ("autre", "Autre"),
    ]

    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100, blank=True)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    subject = models.CharField("Sujet", max_length=50, choices=SUBJECT_CHOICES)
    property_interest = models.CharField(
        "Logement concerné", max_length=50, blank=True
    )
    message = models.TextField("Message")
    terms_accepted = models.BooleanField("CGV acceptées", default=False)
    is_read = models.BooleanField("Lu", default=False)
    created_at = models.DateTimeField("Reçu le", auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.get_subject_display()}"


class NewsletterSubscription(models.Model):
    """Newsletter email subscription."""

    email = models.EmailField("Email", unique=True)
    is_active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField("Inscrit le", auto_now_add=True)

    class Meta:
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class Page(models.Model):
    """Editable static page (About, Legal, Privacy, FAQ, Local Guide)."""

    TEMPLATE_CHOICES = [
        ("about", "À propos"),
        ("contact", "Contact"),
        ("faq", "FAQ"),
        ("local_guide", "Guide local"),
        ("legal", "Mentions légales"),
        ("privacy", "Politique de confidentialité"),
        ("custom", "Personnalisée"),
    ]

    title = models.CharField("Titre", max_length=200)
    slug = models.SlugField("Slug", max_length=200, unique=True)
    template = models.CharField(
        "Template",
        max_length=50,
        choices=TEMPLATE_CHOICES,
        default="custom",
        help_text="Sélectionnez le template à utiliser pour l'affichage",
    )
    content = models.TextField(
        "Contenu",
        blank=True,
        help_text="Contenu de la page (HTML autorisé)",
    )
    meta_title = models.CharField(
        "Meta title", max_length=70, blank=True, help_text="Titre SEO"
    )
    meta_description = models.CharField(
        "Meta description",
        max_length=160,
        blank=True,
        help_text="Description SEO",
    )
    is_published = models.BooleanField("Publiée", default=True)
    order = models.PositiveIntegerField("Ordre", default=0)
    created_at = models.DateTimeField("Créée le", auto_now_add=True)
    updated_at = models.DateTimeField("Mise à jour le", auto_now=True)

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
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
