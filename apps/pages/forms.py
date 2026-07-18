from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    """Public contact form."""

    first_name = forms.CharField(
        label=_("Prénom"),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Votre prénom"),
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Nom"),
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Votre nom"),
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("votre@email.com"),
                "class": "form-control",
            }
        ),
    )
    phone = forms.CharField(
        label=_("Téléphone"),
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("+33 6 00 00 00 00"),
                "class": "form-control",
            }
        ),
    )
    subject = forms.ChoiceField(
        label=_("Sujet"),
        choices=[
            ("", _("— Choisissez un sujet —")),
            ("reservation", _("Réservation")),
            ("information", _("Demande d'information")),
            ("disponibilite", _("Vérification de disponibilité")),
            ("tarif", _("Demande de tarif")),
            ("reclamation", _("Réclamation")),
            ("autre", _("Autre")),
        ],
        widget=forms.Select(attrs={"class": "form-control nice-select"}),
    )
    property_interest = forms.ChoiceField(
        label=_("Logement concerné"),
        required=False,
        choices=[
            ("", _("— Aucun logement spécifique —")),
            ("royan", _("Royan — Appartement Grande Conche")),
            ("villa", _("Saint-Trojan — Villa")),
            ("maison", _("Saint-Trojan — Maison")),
        ],
        widget=forms.Select(attrs={"class": "form-control nice-select"}),
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(
            attrs={
                "placeholder": _("Votre message..."),
                "class": "form-control",
                "rows": 6,
            }
        ),
    )
    accept_terms = forms.BooleanField(
        label=_("J'accepte la politique de confidentialité"),
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class NewsletterForm(forms.Form):
    """Simple newsletter subscription form."""

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("Votre adresse e-mail"),
                "class": "form-control",
            }
        ),
    )
