import requests
from django.conf import settings


def get_coordinates(location):
    """Helper function for Geocoding, with Mapbox API

    Args:
        location (string): Pass in location as string to the url 
        'https://api.mapbox.com/geocoding/v5/mapbox.places/<location>.json?access_token=<mapbox_token>'

    Returns:
        list: returns latitude and longitude coordinates, i.e [-20054, 33625]
    """
    response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={settings.MAPBOX_KEY}')
    data = response.json()
    coordinates = data['features'][0]['center']
    
    return coordinates