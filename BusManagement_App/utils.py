from django.db.models.signals import post_save
from .models import SecondaryAddressRequest, Student,GeocodedAddress
import requests

import logging

logger = logging.getLogger(__name__)


subscription_key= 'tX8QollQ26xGAEAJ6w3YSI3mHjr65fNRkPAgrgn84Q4'

def geocode_address(address, subscription_key):
    base_url = "https://atlas.microsoft.com/search/address/json"
    params = {
        'api-version': '1.0',
        'subscription-key': subscription_key,
        'query': address,
        'format': 'json'
    }
    response = requests.get(base_url, params=params)
    print(response.json())
    print("*******************")
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to geocode address"


# Fonction pour géocoder et enregistrer les adresses des étudiants
def geocode_and_save_addresses(student):
    # Assurez-vous que l'étudiant est éligible pour le transport avant de continuer
    if not student.is_eligible_for_transport:
        return f"L'adresse de l'étudiant {student.address} ne sera pas enregistrée car il/elle n'est pas éligible pour le transport."

    # Récupérer l'adresse de l'étudiant
    address = student.address

    logger.debug(f"Géocodage de l'adresse : {address}")
    # Géocodage de l'adresse
    result = geocode_address(address, subscription_key)
    latitude = result['results'][0]['position']['lat']
    longitude = result['results'][0]['position']['lon']
    print("***************************************")
    print(latitude, longitude)

    # Vérifier si les coordonnées de latitude et de longitude ont été récupérées avec succès
    if latitude is not None and longitude is not None:
        logger.debug(f"Coordonnées géocodées : {latitude}, {longitude}")

        # Créer une nouvelle instance de GeocodedAddress seulement si l'étudiant est éligible
        GeocodedAddress.objects.create(
            original_address=address,
            latitude=latitude,
            longitude=longitude,
            student=student
        )
        return f"L'adresse de l'étudiant {student.address} a été géocodée et enregistrée avec succès."
    else:
        logger.warning(f"Échec du géocodage de l'adresse : {address}")
        return "Échec du géocodage de l'adresse."



def geocode_student_address(sender, instance, created, **kwargs):
    logging.info("******************************************************")
    print("***   *****    ****** created         **    ***********   ***")
    if created:
        logging.info("Signal triggered successfully for new student creation.")
        geocode_and_save_addresses(instance)

post_save.connect(geocode_student_address, sender=Student)


import json

import logging

# Define a logger
logger = logging.getLogger(__name__)

def get_geocoded_addresses_for_map(parent=None):
    # Retrieve geocoded addresses from the database
    if parent:
        geocoded_addresses = GeocodedAddress.objects.filter(student__parent=parent)
        print(f"Filtered Geocoded Addresses for Parent {parent.id}: {list(geocoded_addresses)}")
    else:
        geocoded_addresses = GeocodedAddress.objects.all()
        print("All Geocoded Addresses: ", list(geocoded_addresses))

    # Prepare data in GeoJSON format
    features = []
    for address in geocoded_addresses:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [address.longitude, address.latitude]  # Note: GeoJSON uses [longitude, latitude] order
            },
            "properties": {
                "address": address.original_address,
                "student_name": f"{address.student.first_name} {address.student.last_name}",
                "student_id": address.student.id
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    print("********************************** ici ")
    logger.debug(f"Geojson data: {geojson_data}")
    print(f"Geojson data: {geojson_data}")
    return json.dumps(geojson_data)


def get_second_addresses_for_map(parent=None):

    geocoded_addresses = SecondaryAddressRequest.objects.filter(student__parent=parent)


    # Prepare data in GeoJSON format
    features = []
    for address in geocoded_addresses:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [address.longitude, address.latitude]  # Note: GeoJSON uses [longitude, latitude] order
            },
            "properties": {
                "address": address.address,
                "student_name": f"{address.student.first_name} {address.student.last_name}",
                "student_id": address.student.id
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    print("********************************** here ")
    logger.debug(f"Geojson data: {geojson_data}")
    print(f"Geojson data: {geojson_data}")
    return json.dumps(geojson_data)
