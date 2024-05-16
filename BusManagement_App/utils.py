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
    # Récupérer l'adresse de l'étudiant
    address = student.address
    

    logger.debug(f"Geocoding address: {address}")
    # Géocodage de l'adresse
    result = geocode_address(address,subscription_key)
    latitude = result['results'][0]['position']['lat']
    longitude = result['results'][0]['position']['lon']
    print("***************************************")
    print(latitude,longitude)

    # Vérifier si les coordonnées de latitude et de longitude ont été récupérées avec succès
    if latitude is not None and longitude is not None:
        logger.debug(f"Geocoded coordinates: {latitude}, {longitude}")

        # Créer une nouvelle instance de GeocodedAddress
        GeocodedAddress.objects.create(
            original_address=address,
            latitude=latitude,
            longitude=longitude,
            student=student
            
        )
    else:
        logger.warning(f"Failed to geocode the address: {address}")



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

def get_geocoded_addresses_for_map():
    # Retrieve geocoded addresses from the database
    geocoded_addresses = GeocodedAddress.objects.all()

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
                "student_name": f"{address.student.first_name} {address.student.last_name}"
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    print("**********************************")
    logger.debug(f"Geojson data: {geojson_data}")
    print(f"Geojson data: {geojson_data}")
    return json.dumps(geojson_data)


def get_second_addresses_for_map():
    # Retrieve geocoded addresses from the database
    geocoded_addresses = SecondaryAddressRequest.objects.all()

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
                "student_name": f"{address.student.first_name} {address.student.last_name}"
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    print("**********************************")
    logger.debug(f"Geojson data: {geojson_data}")
    print(f"Geojson data: {geojson_data}")
    return json.dumps(geojson_data)
