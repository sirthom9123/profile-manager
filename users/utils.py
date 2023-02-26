import requests
from django.conf import settings


def get_coordinates(location):
    response = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={settings.MAPBOX_KEY}')
    data = response.json()
    coordinates = data['features'][0]['center']
    
    return coordinates