from django.contrib import admin
from .models import ContactMessage, NewsletterSubscription, Page


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "subject",
        "property_interest",
        "is_read",
        "created_at",
    ]
    list_editable = ["is_read"]
    list_filter = ["is_read", "subject", "created_at"]
    search_fields = ["first_name", "last_name", "email", "message"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        return super().get_queryset(request).defer("message")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "template", "is_published", "order", "updated_at"]
    list_editable = ["is_published", "order"]
    list_filter = ["template", "is_published"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        (
            "Informations",
            {
                "fields": [
                    "title",
                    "slug",
                    "template",
                    "is_published",
                    "order",
                ]
            },
        ),
        (
            "Contenu",
            {
                "fields": ["content"],
                "classes": ["wide"],
            },
        ),
        (
            "SEO",
            {
                "fields": ["meta_title", "meta_description"],
                "classes": ["collapse"],
            },
        ),
    ]


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "created_at"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["email"]
    date_hierarchy = "created_at"
