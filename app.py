from flask import Flask, render_template, redirect, url_for, request
from socket import gethostname, gethostbyname
# from urllib2 import urlopen
from geoip import geolite2
from geoip import open_database
import urllib.request as ur
import urllib
import socket
import requests
import config

app = Flask(__name__)


@app.route('/')
def location():
    # get the user's external IP address
    user_ip = requests.get('http://ip.42.pl/raw').text

    print(user_ip)

    # get location information based off of IP address
    url = 'http://ip-api.com/json/#' + user_ip
    r = requests.get(url)
    js = r.json()
    status = js['status']

    # if call is successful
    if status != 'success':
        return redirect(url_for('error_page'))

    try:
        city = js['city']
        state = js['regionName']
        ip_coordinates = ",".join([js['lat'], js['lon']])

        # pass the coordinates and city name to the route that gets weather info
        return redirect(url_for('weather', ip_coordinates=ip_coordinates, city=city, state=state))
    except KeyError:
        return redirect(url_for('error_page'))


@app.route('/weather/<ip_coordinates>/<city>/<state>')
def weather(ip_coordinates, city, state):
    weather_key = config.weather_key
    degree_sign = u'\N{DEGREE SIGN}'

    # request weather info from the weather API
    # format for weather api request = https://api.darksky.net/forecast/[key]/[latitude],[longitude]
    response = requests.get(
        'https://api.forecast.io/forecast/%s/%s' % (weather_key, ip_coordinates)
    )
    data = response.json()
    # data['hourly'] contains hourly data with the time formatted as Epoch Unix Time - should look into how to display hourly data in weather.html
    # data['hourly']
    weather_icon = str(data['currently']['icon'])
    temperature = str(int(data['currently']['temperature']))
    RAIN_WARNING = data['daily']['data'][0]['precipProbability']

    if RAIN_WARNING == 0:
        rain_commentary = "there is a no chance of rain! It's a sunny day"
    elif 0 < RAIN_WARNING <= .5:
        rain_commentary = "there is a slight chance of rain. You might want to grab an umbrella ☔"
    elif .5 < RAIN_WARNING < .75:
        rain_commentary = "there is a high chance of rain. Grab an umbrella on your way out! ☔"
    elif RAIN_WARNING == 1:
        rain_commentary = "it is raining right now!"
    else:
        rain_commentary = "it is definitely going to rain today! GRAB YOUR UMBRELLA. ☔"
    # str(data['daily']['data'][0]['precipProbability']) + "% chance of rain."

    # print out a statement with the current weather info + location that was used/detected
    # return("Right now in "+ city + ", " + state + " it is " + temperature +  degree_sign + " and there  is a " + RAIN_WARNING)
    location = {'city': city, 'state': state}
    weather_info = {'temperature': temperature, 'rain': rain_commentary}
    return render_template(
        'weather.html', location=location, weather_info=weather_info, weather_icon=weather_icon
    )


@app.errorhandler(404)
def error_page(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
