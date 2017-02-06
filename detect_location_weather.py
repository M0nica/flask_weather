from flask import Flask, render_template, request, redirect, url_for
from geoip import geolite2
from geoip import open_database
import urllib.request as ur
import socket
import requests
import config
import ipgetter

app = Flask(__name__)

@app.route('/')

def location():

    # get the user's IP address
    user_ip = ipgetter.myip()
    print(user_ip)

    # get location information based off of IP address
    url = 'http://freegeoip.net/json/'+user_ip
    r = requests.get(url)
    js = r.json()
    city = js['city']
    state = js['region_name']
    ip_coordinates = str(js['latitude']) + "," + str(js['longitude'])

    #pass the coordinates and city name to the route that gets weather info
    return redirect(url_for('weather', ip_coordinates=ip_coordinates, city=city, state=state))
    # return "hah"
@app.route('/weather/<ip_coordinates>/<city>/<state>')

def weather(ip_coordinates, city, state):
    weather_key = config.weather_key
    degree_sign= u'\N{DEGREE SIGN}'

    # request weather info from the weather API
    # format for weather api request = https://api.darksky.net/forecast/[key]/[latitude],[longitude]
    response = requests.get('https://api.forecast.io/forecast/' + weather_key + '/' + ip_coordinates)
    data = response.json()

    temperature = str(int(data['currently']['temperature']))
    RAIN_WARNING = str(data['daily']['data'][0]['precipProbability']) + "% chance of rain."

    #print out a statement with the current weather info + location that was used/detected
    return("Right now in "+ city + ", " + state + " it is " + temperature +  degree_sign + " and there  is a " + RAIN_WARNING)
if __name__ == '__main__':
    app.run()
