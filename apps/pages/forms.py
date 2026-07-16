from django import forms


class ContactForm(forms.Form):
    """Public contact form."""

    first_name = forms.CharField(
        label="Prénom",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Votre prénom",
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        label="Nom",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Votre nom",
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "votre@email.com",
                "class": "form-control",
            }
        ),
    )
    phone = forms.CharField(
        label="Téléphone",
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "+33 6 00 00 00 00",
                "class": "form-control",
            }
        ),
    )
    subject = forms.ChoiceField(
        label="Sujet",
        choices=[
            ("", "— Choisissez un sujet —"),
            ("reservation", "Réservation"),
            ("information", "Demande d'information"),
            ("disponibilite", "Vérification de disponibilité"),
            ("tarif", "Demande de tarif"),
            ("rec lamation", "Réclamation"),
            ("autre", "Autre"),
        ],
        widget=forms.Select(attrs={"class": "form-control nice-select"}),
    )
    property_interest = forms.ChoiceField(
        label="Logement concerné",
        required=False,
        choices=[
            ("", "— Aucun logement spécifique —"),
            ("royan", "Royan — Appartement Grande Conche"),
            ("villa", "Saint-Trojan — Villa"),
            ("maison", "Saint-Trojan — Maison"),
        ],
        widget=forms.Select(attrs={"class": "form-control nice-select"}),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Votre message...",
                "class": "form-control",
                "rows": 6,
            }
        ),
    )
    accept_terms = forms.BooleanField(
        label="J'accepte la politique de confidentialité",
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class NewsletterForm(forms.Form):
    """Simple newsletter subscription form."""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Votre adresse e-mail",
                "class": "form-control",
            }
        ),
    )
