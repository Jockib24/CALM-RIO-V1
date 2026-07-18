from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Amenity(models.Model):
    """An amenity or feature that a property can have (WiFi, Parking, etc.)."""

    name = models.CharField("Nom", max_length=100)
    icon = models.CharField(
        "Icône FontAwesome",
        max_length=100,
        help_text="Classe FontAwesome (ex: 'fas fa-wifi')",
        blank=True,
    )
    order = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Property(models.Model):
    """A rental property listing."""

    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("published", "Publié"),
        ("hidden", "Masqué"),
    ]

    # Core info
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField(
        "Slug",
        max_length=200,
        unique=True,
        help_text="Identifiant URL unique. Laisser vide pour auto-génération.",
    )
    subtitle = models.CharField("Sous-titre", max_length=300, blank=True)
    summary = models.TextField(
        "Résumé court",
        max_length=500,
        help_text="Affiché sur la page d'accueil et dans les listes",
    )
    description = models.TextField("Description complète")
    status = models.CharField(
        "Statut", max_length=20, choices=STATUS_CHOICES, default="draft"
    )
    featured = models.BooleanField("Mis en avant", default=False)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    # Location
    city = models.CharField("Ville", max_length=100, default="Royan")
    address = models.CharField("Adresse", max_length=300, blank=True)
    latitude = models.FloatField("Latitude", blank=True, null=True)
    longitude = models.FloatField("Longitude", blank=True, null=True)
    distance_to_beach = models.CharField("Distance plage", max_length=100, blank=True)

    # Capacity & dimensions
    max_guests = models.PositiveIntegerField("Voyageurs max", default=4)
    bedrooms = models.PositiveIntegerField("Chambres", default=2)
    beds = models.PositiveIntegerField("Lits", default=2)
    bathrooms = models.PositiveIntegerField("Salles de bain", default=1)
    surface_area = models.CharField(
        "Surface", max_length=100, blank=True, help_text="ex: '60 m² + 20 m²'"
    )

    # Pricing
    base_price = models.DecimalField(
        "Prix de base / nuit", max_digits=8, decimal_places=2, default=0
    )
    cleaning_fee = models.DecimalField(
        "Frais de ménage", max_digits=8, decimal_places=2, blank=True, null=True
    )
    security_deposit = models.DecimalField(
        "Caution", max_digits=8, decimal_places=2, blank=True, null=True
    )
    currency = models.CharField("Monnaie", max_length=10, default="€")

    # Amenities M2M
    amenities = models.ManyToManyField(Amenity, verbose_name="Équipements", blank=True)

    # House rules
    check_in_time = models.CharField(
        "Heure d'arrivée", max_length=50, default="À partir de 16:00"
    )
    check_out_time = models.CharField(
        "Heure de départ", max_length=50, default="Avant 10:00"
    )
    house_rules = models.TextField("Règles de la maison", blank=True)

    # Host info
    host_name = models.CharField("Nom de l'hôte", max_length=100, blank=True)
    registration_number = models.CharField(
        "Numéro d'enregistrement", max_length=50, blank=True
    )

    # SEO
    meta_title = models.CharField(
        "Meta title", max_length=70, blank=True, help_text="Titre SEO (70 car. max)"
    )
    meta_description = models.CharField(
        "Meta description",
        max_length=160,
        blank=True,
        help_text="Description SEO (160 car. max)",
    )

    # Timestamps
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Mis à jour le", auto_now=True)

    class Meta:
        verbose_name = "Propriété"
        verbose_name_plural = "Propriétés"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("properties:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PropertyImage(models.Model):
    """An image belonging to a property."""

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Propriété",
    )
    image = models.ImageField("Image", upload_to="properties/")
    alt_text = models.CharField("Texte alternatif", max_length=200, blank=True)
    is_primary = models.BooleanField("Image principale", default=False)
    order = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["order"]

    def __str__(self):
        return f"Image {self.order} - {self.property.name}"


class Booking(models.Model):
    """A reservation/booking for a property."""

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("confirmed", "Confirmée"),
        ("cancelled", "Annulée"),
        ("completed", "Terminée"),
    ]

    SOURCE_CHOICES = [
        ("direct", "Réservation directe"),
        ("airbnb", "Airbnb"),
        ("booking_com", "Booking.com"),
    ]

    PAYMENT_CHOICES = [
        ("unpaid", "Impayé"),
        ("paid", "Payé"),
        ("refunded", "Remboursé"),
    ]

    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100, blank=True)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    unit = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Propriété",
    )
    check_in = models.DateField("Date d'arrivée")
    check_out = models.DateField("Date de départ")
    guests = models.PositiveIntegerField("Voyageurs", default=1)
    total_price = models.DecimalField(
        "Prix total", max_digits=8, decimal_places=2, default=0
    )
    status = models.CharField(
        "Statut", max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    source = models.CharField(
        "Source", max_length=20, choices=SOURCE_CHOICES, default="direct"
    )
    payment_status = models.CharField(
        "Paiement", max_length=20, choices=PAYMENT_CHOICES, default="unpaid"
    )
    notes = models.TextField("Notes", blank=True)
    created_at = models.DateTimeField("Créée le", auto_now_add=True)
    updated_at = models.DateTimeField("Mise à jour le", auto_now=True)

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name} — {self.unit.name} ({self.check_in})"
        )

    @property
    def nights(self):
        return (self.check_out - self.check_in).days


class ICalSource(models.Model):
    """An iCal URL to sync external calendar data (Airbnb, Booking.com, etc.)."""

    unit = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="ical_sources",
        verbose_name="Propriété",
    )
    name = models.CharField("Nom", max_length=100, help_text="ex: Airbnb, Booking.com")
    url = models.URLField("URL iCal", max_length=500)
    is_active = models.BooleanField("Actif", default=True)
    last_synced = models.DateTimeField("Dernière synchro", null=True, blank=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        verbose_name = "Source iCal"
        verbose_name_plural = "Sources iCal"

    def __str__(self):
        return f"{self.name} — {self.unit.name}"


class BlockedPeriod(models.Model):
    """A date range during which a property is blocked (from iCal sync)."""

    source = models.ForeignKey(
        ICalSource,
        on_delete=models.CASCADE,
        related_name="blocked_periods",
        verbose_name="Source iCal",
    )
    unit = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="blocked_periods",
        verbose_name="Propriété",
    )
    start_date = models.DateField("Date de début")
    end_date = models.DateField("Date de fin")
    external_id = models.CharField(
        "ID externe", max_length=255, blank=True, db_index=True
    )
    summary = models.CharField("Résumé", max_length=255, blank=True)

    class Meta:
        verbose_name = "Période bloquée"
        verbose_name_plural = "Périodes bloquées"
        indexes = [
            models.Index(fields=["unit", "start_date", "end_date"]),
        ]

    def __str__(self):
        return f"{self.unit.name}: {self.start_date} → {self.end_date}"
