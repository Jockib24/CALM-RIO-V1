from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Booking, Property, BlockedPeriod


class BookingRequestForm(forms.Form):
    """Public booking request form — creates a pending booking on submit."""

    property_slug = forms.CharField(widget=forms.HiddenInput())

    first_name = forms.CharField(
        label=_("Prénom"),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Votre prénom"),
                "class": "form-control",
                "required": True,
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
                "required": True,
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
    check_in = forms.DateField(
        label=_("Date d'arrivée"),
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "required": True,
            }
        ),
    )
    check_out = forms.DateField(
        label=_("Date de départ"),
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "required": True,
            }
        ),
    )
    guests = forms.IntegerField(
        label=_("Voyageurs"),
        min_value=1,
        max_value=20,
        initial=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": 1,
                "max": 20,
            }
        ),
    )
    message = forms.CharField(
        label=_("Message (optionnel)"),
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": _("Questions ou demandes particulières..."),
                "class": "form-control",
                "rows": 3,
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        slug = cleaned_data.get("property_slug")

        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError(
                    _("La date de départ doit être postérieure à la date d'arrivée.")
                )

            if check_in < date.today():
                raise forms.ValidationError(
                    _("La date d'arrivée ne peut pas être dans le passé.")
                )

            # Check availability against confirmed bookings + blocked periods
            if slug:
                try:
                    prop = Property.objects.get(slug=slug, status="published")
                except Property.DoesNotExist:
                    raise forms.ValidationError(_("Logement introuvable."))

                # Check confirmed bookings
                from .models import Booking as BookingModel

                overlapping_bookings = BookingModel.objects.filter(
                    unit=prop,
                    status="confirmed",
                    check_in__lt=check_out,
                    check_out__gt=check_in,
                )
                if overlapping_bookings.exists():
                    raise forms.ValidationError(
                        _(
                            "Ce logement n'est pas disponible pour les dates sélectionnées. "
                            "Veuillez choisir d'autres dates ou nous contacter."
                        )
                    )

                # Check blocked periods (iCal)
                overlapping_blocked = BlockedPeriod.objects.filter(
                    unit=prop,
                    start_date__lt=check_out,
                    end_date__gt=check_in,
                )
                if overlapping_blocked.exists():
                    raise forms.ValidationError(
                        _(
                            "Ce logement n'est pas disponible pour les dates sélectionnées "
                            "(période bloquée). Veuillez choisir d'autres dates."
                        )
                    )

        return cleaned_data
