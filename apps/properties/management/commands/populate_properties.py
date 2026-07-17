"""
Management command to populate the 3 rental properties into the database.
Run with: python manage.py populate_properties
"""

from django.core.management.base import BaseCommand
from apps.properties.models import Property, Amenity


class Command(BaseCommand):
    help = "Populate the 3 CalmRio rental properties"

    def handle(self, *args, **options):
        # Create amenities
        amenities_data = [
            {"name": "WiFi haut débit", "icon": "fas fa-wifi", "order": 1},
            {"name": "Parking gratuit", "icon": "fas fa-parking", "order": 2},
            {"name": "Cuisine équipée", "icon": "fas fa-utensils", "order": 3},
            {"name": "Espace télétravail", "icon": "fas fa-laptop", "order": 4},
            {"name": "Animaux acceptés", "icon": "fas fa-paw", "order": 5},
            {"name": "Télévision", "icon": "fas fa-tv", "order": 6},
            {"name": "Ascenseur", "icon": "fas fa-elevator", "order": 7},
            {"name": "Lave-linge", "icon": "fas fa-washing-machine", "order": 8},
            {"name": "Accès plage", "icon": "fas fa-umbrella-beach", "order": 9},
            {"name": "Jardin clos", "icon": "fas fa-tree", "order": 10},
            {"name": "Recharge VE", "icon": "fas fa-charging-station", "order": 11},
            {"name": "Pistes cyclables", "icon": "fas fa-bicycle", "order": 12},
            {"name": "Barbecue", "icon": "fas fa-fire", "order": 13},
            {"name": "Lave-vaisselle", "icon": "fas fa-sink", "order": 14},
            {"name": "Cheminée", "icon": "fas fa-fire", "order": 15},
            {"name": "Cour privée", "icon": "fas fa-tree", "order": 16},
            {"name": "Commerces à pied", "icon": "fas fa-shopping-bag", "order": 17},
        ]

        amenities = {}
        for data in amenities_data:
            amenity, _ = Amenity.objects.update_or_create(
                name=data["name"],
                defaults=data,
            )
            amenities[data["name"]] = amenity

        self.stdout.write(self.style.SUCCESS(f"Created {len(amenities)} amenities"))

        # Properties data
        properties_data = [
            {
                "name": "Appartement — 100m de la Grande Conche",
                "slug": "royan-appartement",
                "subtitle": "Royan, Nouvelle-Aquitaine",
                "summary": "Appartement neuf 60m², 2 chambres, terrasse 20m², à 100m de la Grande Conche. Parking, wifi, espace télétravail.",
                "description": """Appartement neuf de 60 m² avec une terrasse de 20 m² alliant un style bord de plage et contemporain, très lumineux, idéalement situé à 100 m de la plage de la Grande Conche et à proximité de nombreux commerces du centre-ville.

Grande pièce de vie avec salon et cuisine / salle à manger. Canapé confortable, cuisine entièrement équipée avec cave à vin de service. Toutes les fenêtres donnent sur la terrasse (partie salon + partie repas, arborée).

2 chambres : l'une avec un grand lit de 160, télé, espace de travail (écran + câble HDMI) ; l'autre avec 2 petits lits de 90. Salle de bain avec douche à l'italienne, buanderie (lave-linge, sèche-linge, fer et table à repasser). WC indépendant.""",
                "status": "published",
                "featured": True,
                "order": 1,
                "city": "Royan",
                "distance_to_beach": "100m",
                "max_guests": 4,
                "bedrooms": 2,
                "beds": 2,
                "bathrooms": 1,
                "surface_area": "60 m² + 20 m² terrasse",
                "base_price": 130,
                "check_in_time": "À partir de 16:00",
                "check_out_time": "Avant 10:00",
                "house_rules": "Arrivée à partir de 16:00\nDépart avant 10:00\n4 voyageurs maximum\nAnimaux acceptés\nÉquipement bébé disponible sur demande",
                "host_name": "Mélanie",
                "registration_number": "173060015134Z",
                "meta_title": "Appartement neuf 4 pers — 100m Grande Conche — Royan | CalmRio",
                "meta_description": "Location vacances Royan : appartement neuf 60m², 2 chambres, terrasse 20m², à 100m de la Grande Conche. Parking, wifi, espace télétravail.",
                "amenities_names": [
                    "WiFi haut débit",
                    "Parking gratuit",
                    "Cuisine équipée",
                    "Espace télétravail",
                    "Animaux acceptés",
                    "Télévision",
                    "Ascenseur",
                    "Lave-linge",
                    "Accès plage",
                ],
            },
            {
                "name": "Villa 6 pers — Jardin clos & terrasses",
                "slug": "saint-trojan-villa",
                "subtitle": "Saint-Trojan-les-Bains, Île d'Oléron",
                "summary": "Villa neuve 110m² pour 6 personnes. Jardin clos, 2 terrasses, plage à vélo, télétravail, animaux acceptés.",
                "description": """Maison neuve au style Oléronais, alliant le style insulaire charentais et contemporain, très lumineuse, avec de beaux volumes, idéalement située entre mer et forêt.

110 m² sur un jardin arboré et clos, avec terrasse en bois 50 m² plein sud (salon de jardin, parasol) et terrasse couverte 17 m² (table en teck). Barbecue. Vaste salon/salle à manger avec grande hauteur sous plafond, baies vitrées sur terrasses. Cuisine ouverte équipée : lave-vaisselle, réfrigérateur, four, micro-ondes, plaque à induction. Cellier avec lave-linge, sèche-linge et congélateur.

3 chambres de 12 m² : 2 avec lit de 160, 1 avec 2 lits de 80. Salle de bain avec douche à l'italienne, WC suspendu indépendant. Draps et serviettes fournis. Prise recharge voiture électrique/hybride (supplément selon relevé de compteur). Bureau et écran HDMI pour télétravail.""",
                "status": "published",
                "featured": True,
                "order": 2,
                "city": "Saint-Trojan-les-Bains",
                "distance_to_beach": "À vélo",
                "max_guests": 6,
                "bedrooms": 3,
                "beds": 4,
                "bathrooms": 1,
                "surface_area": "110 m²",
                "base_price": 180,
                "check_in_time": "Entre 16:00 et 20:00",
                "check_out_time": "Avant 10:00",
                "house_rules": "Arrivée entre 16:00 et 20:00\nDépart avant 10:00\n6 voyageurs maximum\nAnimaux acceptés\nRecharge voiture électrique avec supplément selon relevé de compteur\nÉquipement bébé disponible sur demande",
                "host_name": "Agnès",
                "registration_number": "17411000371D4",
                "meta_title": "Villa neuve 6 pers Oléron — jardin clos & terrasses | Saint-Trojan | CalmRio",
                "meta_description": "Villa neuve 110m² à Saint-Trojan-les-Bains pour 6 personnes. Jardin clos, 2 terrasses, plage à vélo, télétravail, animaux acceptés.",
                "amenities_names": [
                    "WiFi haut débit",
                    "Parking gratuit",
                    "Cuisine équipée",
                    "Espace télétravail",
                    "Animaux acceptés",
                    "Jardin clos",
                    "Recharge VE",
                    "Pistes cyclables",
                    "Barbecue",
                    "Lave-linge",
                    "Lave-vaisselle",
                ],
            },
            {
                "name": "Maison 6 pers — Cour privée",
                "slug": "saint-trojan-maison",
                "subtitle": "Saint-Trojan-les-Bains, Île d'Oléron",
                "summary": "Maison de village 75m² rénovée pour 6 personnes. Cour privée, 3 chambres, à 10 min des plages. Proche pistes cyclables.",
                "description": """Maison de village entièrement rénovée, au calme, avec 3 chambres dont une au rez-de-chaussée, séjour très lumineux et agréable avec cheminée. La maison dispose d'une jolie cour privée avec salon de jardin et parasol, idéale pour les petits-déjeuners au soleil ou les repas en plein air.

À pied des commerces, à vélo de la plage et de la forêt, la localisation est idéale pour explorer l'île d'Oléron. Le marché couvert de Saint-Trojan (produits frais, huîtres, poissons) est à 5 min à pied.

3 chambres : 1 avec lit double 160 (RDC), 2 avec lits doubles 140 (étage). Salle de bain avec douche, WC séparé. Cuisine équipée ouverte sur le séjour : gazinière, réfrigérateur/congélateur, lave-linge, micro-ondes.""",
                "status": "published",
                "featured": True,
                "order": 3,
                "city": "Saint-Trojan-les-Bains",
                "distance_to_beach": "10 min à pied",
                "max_guests": 6,
                "bedrooms": 3,
                "beds": 3,
                "bathrooms": 1,
                "surface_area": "75 m²",
                "base_price": 150,
                "check_in_time": "Entre 15:00 et 19:00",
                "check_out_time": "Avant 11:00",
                "house_rules": "Arrivée entre 15:00 et 19:00\nDépart avant 11:00\n6 voyageurs maximum\nAnimaux non acceptés\nNon-fumeur (possible en extérieur)",
                "host_name": "Marie",
                "registration_number": "17411000372D2",
                "meta_title": "Maison de village 6 pers — cour privée | Saint-Trojan | CalmRio",
                "meta_description": "Maison de village 75m² rénovée à Saint-Trojan-les-Bains pour 6 personnes. Cour privée, 3 chambres, à 10 min des plages.",
                "amenities_names": [
                    "WiFi haut débit",
                    "Cuisine équipée",
                    "Cheminée",
                    "Commerces à pied",
                    "Pistes cyclables",
                    "Accès plage",
                    "Lave-linge",
                    "Parking gratuit",
                ],
            },
        ]

        for data in properties_data:
            amenity_names = data.pop("amenities_names")
            property_obj, created = Property.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            # Set amenities
            property_obj.amenities.clear()
            for name in amenity_names:
                if name in amenities:
                    property_obj.amenities.add(amenities[name])

            status = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{status}: {property_obj.name}"))

        self.stdout.write(self.style.SUCCESS("\nDone! All properties populated."))
