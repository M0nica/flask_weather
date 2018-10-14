# coding=utf-8
import requests
import json
from flask import Flask, session, render_template, redirect, url_for, send_from_directory
import os

app = Flask(__name__, static_folder="./build")

app.secret_key = os.environ['secret_key']

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("./build/" + path):
        return send_from_directory('./build', path)
    else:
        return send_from_directory('./build', 'index.html')

@app.route('/getLocationByIP', methods=['GET'])
def location():
    if (session and session['ip_info']):
        data = session['ip_info']
        return json.dumps(data)
    else:
        data = get_ip_info()
        session['ip_info'] = data

        return json.dumps(data)


def celsius():
    if hasattr(os.environ, "celsius"):
        if os.environ['celsius']:
            return "?units=si"

    return ""


@app.route('/weather/<ip>')
def weather(ip):
    weather_key = os.environ['weather_key']
    # degree_sign = u'\N{DEGREE SIGN}'

    # request weather info from the weather API
    # format for weather api request =
    # https://api.darksky.net/forecast/[key]/[latitude],[longitude]
    response = requests.get(
        'https://api.forecast.io/forecast/%s/%s%s' % (
            weather_key, ip, celsius()
        )
    )
    data = response.json()

    # data['hourly'] contains hourly data with the time formatted as Epoch
    # Unix Time - should look into how to display hourly data in weather.html
    # data['hourly']

    weather_icon = str(data['currently']['icon'])
    temperature = str(int(data['currently']['temperature']))
    RAIN_WARNING = data['daily']['data'][0]['precipProbability']

    if RAIN_WARNING == 0:
        rain_commentary = "there is a no chance of rain! It's a sunny day"
    elif 0 < RAIN_WARNING <= .5:
        rain_commentary = "there is a slight chance of rain. " \
                          "You might want to grab an umbrella ☔"
    elif .5 < RAIN_WARNING < .75:
        rain_commentary = "there is a high chance of rain. " \
                          "Grab an umbrella on your way out! ☔"
    elif RAIN_WARNING == 1:
        rain_commentary = "it is raining right now!"
    else:
        rain_commentary = "it is definitely going to rain today! " \
                          "GRAB YOUR UMBRELLA. ☔"
    # str(data['daily']['data'][0]['precipProbability']) + "% chance of rain."


    weather_info = {'temperature': temperature, 'rainCommentary': rain_commentary, "icon": weather_icon, "hasCelsius": celsius() }
    return json.dumps(weather_info)

@app.errorhandler(404)
def error_page(error):
    return render_template('404.html'), 404


# private non-route methods
def get_ip_info():
    ip = requests.get('http://ip.42.pl/raw').text
    r = requests.get('http://ip-api.com/json/#' + ip)
    js = r.json()

    return {
        'success': js['status'] == 'success',
        'city': js['city'],
        'state': js['regionName'],
        'ip_coords': str(js['lat']) + ", " + str(js['lon'])
    }


if __name__ == '__main__':
    app.run()
