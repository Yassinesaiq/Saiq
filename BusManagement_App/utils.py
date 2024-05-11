from azure.maps.search import MapsSearchClient
from azure.core.credentials import AzureKeyCredential
from azure.maps.geolocation import MapsGeolocationClient
from azure.identity import DefaultAzureCredential
from django.db.models.signals import post_save
from .models import Student,GeocodedAddress
import requests

import logging

logger = logging.getLogger(__name__)


# Créez une instance de MapsSearchClient avec votre clé d'abonnement Azure Maps
# credential = AzureKeyCredential("fo42NIlUsCF72sSrXlAIFCukuuqZ5fN7OQgg52JLPlA")
# search_client = MapsSearchClient(credential=credential)
subscription_key= 'fo42NIlUsCF72sSrXlAIFCukuuqZ5fN7OQgg52JLPlA'

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
            longitude=longitude
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