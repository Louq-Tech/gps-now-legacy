'''
Currently not in use due to it's inconsistency in providing information which leads to bugs
'''

from geopy.geocoders import Nominatim

def location_provider(latitude, longitude):
    geolocator = Nominatim(user_agent="location_finder")

    location = geolocator.reverse([latitude, longitude], exactly_one=True, language='en')

    address_components = location.raw['address']
    
    locality = address_components.get('suburb', '') or \
               address_components.get('neighbourhood', '') or \
               address_components.get('town', '') or \
               address_components.get('village', '') or \
               address_components.get('hamlet', '') or \
               address_components.get('subward', '')
    city = address_components.get('city', '')

    location_string = f"{locality}, {city}"

    return location_string
