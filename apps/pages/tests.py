from django.test import TestCase
from django.urls import reverse

from apps.pages.models import ContactMessage, NewsletterSubscription, SiteText, Page


class SiteTextModelTest(TestCase):
    def setUp(self):
        self.text = SiteText.objects.create(
            key="hero_title",
            label="Titre du hero",
            translations={"fr": "Bienvenue", "en": "Welcome"},
        )

    def test_site_text_creation(self):
        self.assertEqual(str(self.text), "Titre du hero")

    def test_get_text_french(self):
        self.assertEqual(self.text.get_text("fr"), "Bienvenue")

    def test_get_text_english(self):
        self.assertEqual(self.text.get_text("en"), "Welcome")

    def test_get_text_fallback(self):
        self.assertEqual(self.text.get_text("es"), "Bienvenue")

    def test_get_text_empty(self):
        empty = SiteText.objects.create(key="empty", label="Empty")
        self.assertEqual(empty.get_text("fr"), "")


class ContactMessageModelTest(TestCase):
    def setUp(self):
        self.msg = ContactMessage.objects.create(
            first_name="Jean",
            last_name="Dupont",
            email="jean@example.com",
            subject="information",
            message="Bonjour, j'aimerais des informations.",
            terms_accepted=True,
        )

    def test_contact_message_str(self):
        expected = "Jean Dupont — Demande d'information"
        self.assertEqual(str(self.msg), expected)

    def test_contact_message_defaults(self):
        self.assertFalse(self.msg.is_read)

    def test_contact_message_terms_accepted(self):
        self.assertTrue(self.msg.terms_accepted)


class NewsletterSubscriptionModelTest(TestCase):
    def setUp(self):
        self.sub = NewsletterSubscription.objects.create(
            email="test@example.com",
        )

    def test_newsletter_creation(self):
        self.assertEqual(str(self.sub), "test@example.com")
        self.assertTrue(self.sub.is_active)

    def test_newsletter_unique_email(self):
        with self.assertRaises(Exception):
            NewsletterSubscription.objects.create(email="test@example.com")


class AboutViewTest(TestCase):
    def test_about_view_status_code(self):
        response = self.client.get(reverse("pages:about"))
        self.assertEqual(response.status_code, 200)

    def test_about_view_template(self):
        response = self.client.get(reverse("pages:about"))
        self.assertTemplateUsed(response, "pages/about.html")


class ContactViewTest(TestCase):
    def test_contact_view_status_code(self):
        response = self.client.get(reverse("pages:contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_template(self):
        response = self.client.get(reverse("pages:contact"))
        self.assertTemplateUsed(response, "pages/contact.html")

    def test_contact_form_submission(self):
        data = {
            "first_name": "Marie",
            "email": "marie@example.com",
            "subject": "information",
            "message": "Test message",
            "accept_terms": True,
        }
        response = self.client.post(reverse("pages:contact"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)


class FaqViewTest(TestCase):
    def test_faq_view(self):
        response = self.client.get(reverse("pages:faq"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/faq.html")


class LocalGuideViewTest(TestCase):
    def test_local_guide_view(self):
        response = self.client.get(reverse("pages:local_guide"))
        self.assertEqual(response.status_code, 200)


class LegalPagesViewTest(TestCase):
    def test_mentions_view(self):
        response = self.client.get(reverse("pages:mentions"))
        self.assertEqual(response.status_code, 200)

    def test_privacy_view(self):
        response = self.client.get(reverse("pages:privacy"))
        self.assertEqual(response.status_code, 200)


class NewsletterViewTest(TestCase):
    def test_newsletter_subscription(self):
        response = self.client.post(
            reverse("pages:newsletter"),
            {"email": "new@example.com"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NewsletterSubscription.objects.count(), 1)

    def test_newsletter_duplicate(self):
        NewsletterSubscription.objects.create(email="dup@example.com")
        response = self.client.post(
            reverse("pages:newsletter"),
            {"email": "dup@example.com"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        # Should still be 1 (get_or_create)
        self.assertEqual(NewsletterSubscription.objects.count(), 1)


class RobotsViewTest(TestCase):
    def test_robots_txt(self):
        response = self.client.get(reverse("pages:robots"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disallow: /admin/")
        self.assertContains(response, "Sitemap:")
        self.assertEqual(response["Content-Type"], "text/plain")


class PageModelTest(TestCase):
    def setUp(self):
        self.page = Page.objects.create(
            title="À propos",
            slug="a-propos",
            template="about",
            content="<p>Notre histoire</p>",
            is_published=True,
        )

    def test_page_creation(self):
        self.assertEqual(str(self.page), "À propos")

    def test_page_absolute_url(self):
        url = self.page.get_absolute_url()
        self.assertIn("about", url)

    def test_page_unpublished(self):
        hidden = Page.objects.create(
            title="Hidden",
            slug="hidden-page",
            template="custom",
            is_published=False,
        )
        self.assertFalse(hidden.is_published)
