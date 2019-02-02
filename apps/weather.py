from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
from json import load


# call back for weather getting
def get_info_send_message(weather_res, address):
    # get temp and convert from kelvin to farenheit
    temp = (((weather_res['main']['temp'])*1.8) - 459.67)
    # get desc
    text = weather_res['weather'][0]['main']

    return "It is {0:0.2f} degrees and {1} at {2}".format(temp, text, address)


# get address
def get_address(weather_lookup_res):
    g_api_key = 'AIzaSyDzAuaakKOwFLZNOagt_7-l9YWS6tOZ7Pc'
    lat, lon = weather_lookup_res['coord']['lat'], weather_lookup_res['coord']['lon']
    with urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}".format(lat, lon, g_api_key)) as a:
        return get_info_send_message(weather_lookup_res, load(a)['results'][0]['formatted_address'])


# get weather
def get_weather(city):
    # use urlencode to take care of cities with whitespace
    key = '52300ccf7c68e789f80942dfa03ec53a'
    try:
        with urlopen("http://api.openweathermap.org/data/2.5/weather?{},us&APPID={}".format(urlencode({'q': city}), key)) as f:
            return get_address(load(f))
    except HTTPError:
        return "Error. Check your spelling."
