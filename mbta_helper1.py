
# from config import MAPQUEST_API_KEY, MBTA_API_KEY
# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = 'oyo5kKGI69WA0NjqYvijQTSAAq4QsBMo'
MBTA_API_KEY = '5951a02b287a4bcaa87ac1e2c37f9a75'

import urllib.request
import urllib.parse
import json
from pprint import pprint

# A little bit of scaffolding if you want to use it


def get_json(location):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.

    Both get_lat_long() and get_nearest_station() might need to use this function.
    """

    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={location}'
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding API URL formatting requirements.
    """
    my_data = urllib.parse.urlencode({
        'location': place_name,
        'key': MAPQUEST_API_KEY
    })
    url = f'{MAPQUEST_BASE_URL}?{my_data}'
    response_data = get_json(url)
    return response_data['results'][0]['locations'][0]['displayLatLng']['lat'], response_data['results'][0]['locations'][0]['displayLatLng']['lng']


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """

    url = f'https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&page%5Blimit%5D=1&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}'
    f = urllib.request.urlopen(url)
    response_text2 = f.read().decode('utf-8')
    response_data2 = json.loads(response_text2)
    # pprint(response_data)
    station = response_data2['data'][0]['attributes']['name']
    Wheelchair = response_data2['data'][0]['attributes']['wheelchair_boarding']
    t = (station, Wheelchair)
    print(t)


def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    latitude, longtitude = get_lat_long(place_name)
    return get_nearest_station(latitude, longtitude)


def main():
    """
    You can test all the functions here
    """
    get_nearest_station('41.5365044','-73.7456555')
    # find_stop_near('Mariel')


if __name__ == '__main__':
    main()