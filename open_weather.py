# https://openweathermap.org/current
import os
import requests
import json
import math

key = os.getenv('OpenweatherAPIkey')
home_city = 'Marschalkenzimmern'
ISO_countrycode_home_city = 'DE'
temp_wanted = 20


def main():
    current_lat, current_lon = get_coord_loc(home_city, ISO_countrycode_home_city, key)
    current_lat = current_lat[0]
    current_lon = current_lon[0]
    current_weather = get_temp(current_lat, current_lon, key)
    current_min_temp = current_weather['main']['temp_min']
    desired_temp = current_min_temp
    radius = 500
    number_coord = 10

    while desired_temp <= temp_wanted:
        print('Run with ' + str(radius) + ' radius and ' + str(number_coord) + ' numbers of coordinates')
        result_coordinates = generate_coordinates(current_lat, current_lon, radius, number_coord)
        places_above_temp_wanted = {}

        for coord in result_coordinates:
            possible_weather = get_temp(coord['latitude'], coord['longitude'], key)
            if possible_weather['main']['temp_min'] >= temp_wanted:
                places_above_temp_wanted.update({possible_weather['name']: possible_weather['main']['temp_min']})
                desired_temp = possible_weather['main']['temp_min']
        if len(places_above_temp_wanted) > 0:
            max_temp = max(places_above_temp_wanted.values())
            city = max(places_above_temp_wanted, key=places_above_temp_wanted.get)
            print(city)
            print(max_temp)

        radius += 100
        number_coord += 10


# Return current longitude and latitude when cityname and ISO2 countrycode is given
def get_coord_loc(cityname, countrycode, apikey):
    location_uri = 'http://api.openweathermap.org/geo/1.0/direct?q={cityname},{countrycode}&limit={limit}&appid={APIkey}' \
        .format(cityname=cityname, countrycode=countrycode, limit=5, APIkey=apikey)
    response_location = requests.get(location_uri)

    if response_location.status_code == 200:
        location_list = json.loads(response_location.text)
        print(location_list)
        current_lat = [location['lat'] for location in location_list]
        current_lon = [location['lon'] for location in location_list]
        return current_lat, current_lon
    else:
        print('Error: Request failed with status code', response_location.status_code)


def get_temp(lat, lon, apikey):
    weather_uri = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APIkey}&units=metric' \
        .format(lat=lat, lon=lon, APIkey=apikey)
    try:
        response_weather = requests.get(weather_uri)

        if response_weather.status_code == 200:
            weather_dict = json.loads(response_weather.text)
            return weather_dict
        else:
            print('Error: Request failed with status code', response_weather.status_code)

    except requests.exceptions.RequestException as e:
        print('Error: It failed because of:', str(e))


# chat gpt suggestion for generating lat/lon coordinates in a radius around a location
def generate_coordinates(start_lat, start_lon, distance, num_points):
    coordinates = []

    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        dx = distance * math.cos(angle)
        dy = distance * math.sin(angle)

        new_lat = start_lat + (180 / math.pi) * (dy / 6371)
        new_lon = start_lon + (180 / math.pi) * (dx / (6371 * math.cos(math.radians(start_lat))))

        coordinates.append({'latitude': new_lat, 'longitude': new_lon})

    return coordinates


main()

# ToDo:
#       try to build an app that looks for the nearest (GoogleMaps Routes API) 20°C warm location
#       get distance to nearest location with GoogleMaps Routes API
#       maybe clean locations on islands...
