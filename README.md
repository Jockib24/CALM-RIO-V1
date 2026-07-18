# CalmRio

**Locations de vacances premium à Royan & Île d'Oléron.**

Site vitrine multilingue (FR/EN/ES/NL) avec réservation directe, tableau de bord de gestion et synchronisation iCal multi-plateforme.

---

## Stack

| Couche | Technologie |
|--------|-------------|
| **Framework** | Django 4.2 LTS |
| **Base de données** | SQLite (dev) / PostgreSQL (prod) |
| **Frontend** | Bootstrap 5, jQuery, CSS custom (Luxivo template) |
| **Internationalisation** | Django i18n (4 langues) |
| **Dashboard** | Django class-based views, CSS custom |
| **iCal** | `icalendar` + `requests` |

## Structure du projet

```
CALM-RIO-V1/
├── apps/
│   ├── home/              # Page d'accueil
│   ├── pages/             # Pages statiques & formulaires (contact, FAQ, mentions, guide local)
│   ├── properties/        # Biens, images, réservations, sources iCal, synchro
│   └── dashboard/         # Tableau de bord admin (messages, newsletter, réservations, iCal)
├── assets/                # Static files (CSS, JS, images, fonts)
├── config/
│   └── settings/          # Settings Django (base.py + environnements)
├── locale/                # Traductions (fr, en, es, nl)
├── templates/             # Templates Django
│   └── dashboard/         # Interface d'administration
└── media/                 # Uploads (images propriétés)
```

## Fonctionnalités

### Site public
- **Page d'accueil** — Hero, présentation des biens, CTA
- **3 fiches propriétés** — Appartement Royan, Villa & Maison Saint-Trojan
  - Galerie photos, équipements, disponibilité, tarifs
- **Guide local** — Plages, activités, restaurants
- **Contact** — Formulaire avec sélection du sujet
- **Newsletter** — Inscription
- **Multilingue** — FR (défaut), EN, ES, NL
- **SEO** — Balises meta, Open Graph, données structurées JSON-LD

### Dashboard (`/dashboard/`)
- **Statistiques** — Messages non lus, réservations actives, abonnés, revenus
- **Messages** — Liste avec filtres (statut, sujet), marquage lu/non lu
- **Newsletter** — Liste des abonnés, activation/désactivation, export CSV
- **Réservations** — CRUD complet, changement de statut inline, calendrier mensuel
- **Calendrier** — Vue mensuelle avec réservations + blocages iCal
- **Propriétés** — Statistiques par bien

### Synchronisation iCal
Synchronise automatiquement les dates bloquées depuis Airbnb, Booking.com, Abritel, etc. via leurs liens iCal.

**Modèles :**
- `ICalSource` — Lien iCal par propriété (nom, URL, actif, dernière synchro)
- `BlockedPeriod` — Périodes bloquées importées (date début/fin, source, UID)

**Commande de synchro :**
```bash
python manage.py sync_ical
```

Options : `--property=ID`, `--source=ID`, `--clear`

Les périodes bloquées apparaissent dans le calendrier du dashboard (rose).

## Installation

```bash
# Cloner
git clone <url> && cd CALM-RIO-V1

# Environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Dépendances
pip install -r requirements.txt

# Variables d'environnement
cp .env.example .env   # adapter

# Base de données
python manage.py migrate
python manage.py populate_properties

# Superuser
python manage.py createsuperuser

# Traductions (optionnel)
python manage.py compilemessages

# Lancer
python manage.py runserver
```

## Commandes utiles

```bash
# Peupler les propriétés
python manage.py populate_properties

# Synchroniser les calendriers iCal
python manage.py sync_ical

# Traductions
python manage.py makemessages -l en -l es -l nl
python manage.py compilemessages
```

## Configuration

Principales variables d'environnement (`.env`) :

| Variable | Description |
|----------|-------------|
| `DJANGO_SETTINGS_MODULE` | Module de settings |
| `SECRET_KEY` | Clé secrète Django |
| `DATABASE_URL` | URL de connexion PostgreSQL (optionnel) |
| `DEBUG` | Mode debug (True/False) |

## License

Propriétaire — CalmRio
