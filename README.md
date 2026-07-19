# CalmRio

**Locations de vacances premium à Royan & Île d'Oléron.**

Site vitrine multilingue (FR/EN/ES/NL) avec réservation directe, tableau de bord de gestion complet et synchronisation iCal multi-plateforme.

---

## Stack

| Couche | Technologie |
|--------|-------------|
| **Framework** | Django 4.2 LTS |
| **Base de données** | SQLite (dev) / PostgreSQL (prod) |
| **Frontend** | Bootstrap 5, jQuery, CSS custom |
| **Internationalisation** | Django i18n (4 langues) |
| **Dashboard** | Django class-based views, CSS design system |
| **Graphiques** | Chart.js (revenus, réservations, taux d'occupation) |
| **iCal** | `icalendar` + `requests` |
| **Email** | Django templated email (confirmation réservations) |

## Structure du projet

```
CALM-RIO-V1/
├── apps/
│   ├── home/              # Page d'accueil
│   ├── pages/             # Pages statiques & formulaires (contact, FAQ, mentions, guide local)
│   ├── properties/        # Biens, images, réservations, sources iCal, saisons, synchro
│   └── dashboard/         # Tableau de bord admin complet
├── assets/                # Static files (CSS, JS, images, fonts)
├── config/
│   └── settings/          # Settings Django (base.py + environnements)
├── locale/                # Traductions (fr, en, es, nl)
├── templates/
│   ├── pages/             # Templates publics
│   └── dashboard/         # Interface d'administration (22 templates)
├── media/                 # Uploads (images propriétés)
└── requirements.txt       # Dépendances Python
```

## Fonctionnalités

### Site public
- **Page d'accueil** — Hero slider, présentation des biens, CTA
- **3 fiches propriétés** — Appartement Royan, Villa & Maison Saint-Trojan
  - Galerie photos responsive, équipements, disponibilité, tarifs
- **Guide local** — Plages, activités, restaurants
- **Contact** — Formulaire avec sélection du sujet
- **Newsletter** — Inscription
- **Multilingue** — FR (défaut), EN, ES, NL
- **SEO** — Balises meta, Open Graph, données structurées JSON-LD

### Dashboard (`/dashboard/`)

#### Accueil & Statistiques
- **Tableau de bord** — KPIs (messages non lus, réservations actives, abonnés, revenus du mois)
- **Graphiques Chart.js** — Revenus mensuels (12 mois), répartition par statut, évolution mensuelle, taux d'occupation par propriété
- **Statut iCal** — Dernière synchronisation par source, sources actives/inactives

#### Gestion des messages
- **Messagerie** — Liste avec filtres (statut: tous/non lus/lus, sujet)
- **Détail message** — Vue complète avec boutons marquer lu/non lu/supprimer
- **Marquage rapide** — Lecture individuelle ou en lot

#### Newsletter
- **Liste abonnés** — Filtrage par statut, export CSV
- **Désactivation** — Activation/désactivation sans suppression

#### Réservations & Tarification
- **Réservations** — CRUD complet, changement de statut inline
- **Calendrier** — Vue mensuelle avec réservations + blocages iCal
- **Facturation** — Montant, statut paiement, devise (EUR)
- **Confirmation email** — Envoi automatique de confirmation par email lors de la création d'une réservation

#### Saisons & Tarification
- **Saisons** — CRUD des saisons (haute, moyenne, basse) avec couleurs distinctes
- **Tarification** — Prix par nuit par saison, applicabilité jours de la semaine
- **Blocage rapide dates** — Blocage direct sans passer par iCal

#### Biens & Propriétés
- **Propriétés** — Liste avec statut actif/inactif, nbres de photos, nbres de blocages
- **Statistiques par bien** — Occupancy, revenus, activité iCal par propriété

#### Annuaire clients
- **Clients** — Liste des guests (nom, email, téléphone)
- **Détail client** — Fiche complète avec historique des réservations

#### Synchronisation iCal
- **Gestion des sources iCal** — CRUD complet (nom, URL, propriété associée, statut actif/inactif)
- **Synchronisation** — Bouton Sync sur chaque source, synchronisation manuelle ou automatique
- **Blocages importés** — Les périodes bloquées apparaissent en rose dans le calendrier

### Synchronisation iCal

Synchronise automatiquement les dates bloquées depuis Airbnb, Booking.com, Abritel, etc. via leurs liens iCal.

**Modèles :**
- `ICalSource` — Lien iCal par propriété (nom, URL, actif, dernière synchro)
- `BlockedPeriod` — Périodes bloquées importées (date début/fin, source, UID)
- `Season` — Saisons tarifaires (nom, couleur, dates, prix/nuit)

**Commande de synchro :**
```bash
python manage.py sync_ical
```

Options : `--source=ID`, `--clear`

**Via le dashboard :**
Le bouton Sync sur `/dashboard/properties/stats/` déclenche la synchronisation pour chaque source iCal individuellement.

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

# Synchroniser une source spécifique
python manage.py sync_ical --source=2

# Réinitialiser avant synchro
python manage.py sync_ical --clear

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

## Pages du Dashboard

| URL | Description |
|-----|-------------|
| `/dashboard/` | Accueil avec KPIs et graphiques |
| `/dashboard/messages/` | Messagerie (filtres statut/sujet) |
| `/dashboard/newsletter/` | Gestion abonnés newsletter |
| `/dashboard/reservations/` | Liste des réservations |
| `/dashboard/calendar/` | Calendrier mensuel |
| `/dashboard/properties/` | Liste des propriétés |
| `/dashboard/properties/stats/` | Statistiques par bien + iCal |
| `/dashboard/properties/saisons/` | Gestion des saisons tarifaires |
| `/dashboard/clients/` | Annuaire clients |
| `/dashboard/profile/` | Mon profil |
| `/dashboard/sitetext/` | Textes du site |
| `/dashboard/ical_sources/` | Gestion sources iCal |

## License

Propriétaire — CalmRio
