from django.contrib import admin
from django.utils.html import format_html
from .models import Amenity, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ["image", "alt_text", "is_primary", "order"]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "order"]
    list_editable = ["order"]
    search_fields = ["name"]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "city",
        "max_guests",
        "base_price",
        "status",
        "featured",
        "order",
        "thumbnail_preview",
    ]
    list_editable = ["status", "featured", "order"]
    list_filter = ["status", "featured", "city"]
    search_fields = ["name", "city", "summary", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at", "thumbnail_preview"]
    inlines = [PropertyImageInline]
    fieldsets = [
        (
            "Informations générales",
            {
                "fields": [
                    "name",
                    "slug",
                    "subtitle",
                    "summary",
                    "description",
                    "status",
                    "featured",
                    "order",
                ]
            },
        ),
        (
            "Localisation",
            {
                "fields": [
                    "city",
                    "address",
                    "latitude",
                    "longitude",
                    "distance_to_beach",
                ]
            },
        ),
        (
            "Capacité & Surface",
            {
                "fields": [
                    "max_guests",
                    "bedrooms",
                    "beds",
                    "bathrooms",
                    "surface_area",
                ]
            },
        ),
        (
            "Tarification",
            {
                "fields": [
                    "base_price",
                    "cleaning_fee",
                    "security_deposit",
                    "currency",
                ]
            },
        ),
        (
            "Équipements",
            {"fields": ["amenities"]},
        ),
        (
            "Règles & Hôte",
            {
                "fields": [
                    "check_in_time",
                    "check_out_time",
                    "house_rules",
                    "host_name",
                    "registration_number",
                ]
            },
        ),
        (
            "SEO",
            {
                "fields": [
                    "meta_title",
                    "meta_description",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Méta-données",
            {
                "fields": ["created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    def thumbnail_preview(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary and primary.image:
            return format_html(
                '<img src="{}" style="width:80px;height:60px;object-fit:cover;border-radius:4px;" />',
                primary.image.url,
            )
        return "—"

    thumbnail_preview.short_description = "Aperçu"


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "property", "is_primary", "order", "image_preview"]
    list_editable = ["is_primary", "order"]
    list_filter = ["property", "is_primary"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px;height:60px;object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"

    image_preview.short_description = "Aperçu"
