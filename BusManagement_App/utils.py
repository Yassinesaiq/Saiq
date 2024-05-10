from azure.maps.search import MapsSearchClient
from azure.core.credentials import AzureKeyCredential
from azure.maps.geolocation import MapsGeolocationClient
from azure.identity import DefaultAzureCredential

from .models import GeocodedAddress
import logging

logger = logging.getLogger(__name__)

credential = DefaultAzureCredential()
geolocation_client = MapsGeolocationClient(
    client_id="c397b87b-3e20-4b57-bab8-fffcbc829e34",
    credential=credential
)
# Créez une instance de MapsSearchClient avec votre clé d'abonnement Azure Maps
credential = AzureKeyCredential("I1_KytP9o2H33JFvrEILeh9wVCmcp6tc5i0ECU_obg0")
search_client = MapsSearchClient(credential=credential)


def geocode_address(address):
    # Utilisez la méthode correcte 'search_address'
    result = search_client.search_address(address=address)
    if result:
        latitude = result.results[0].position.lat
        longitude = result.results[0].position.lon
        return latitude, longitude
    else:
        return None, None

# Fonction pour géocoder et enregistrer les adresses des étudiants
def geocode_and_save_addresses(student):
    # Récupérer l'adresse de l'étudiant
    address = student.address

    logger.debug(f"Geocoding address: {address}")

    # Géocodage de l'adresse
    latitude, longitude = geocode_address(address)

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