import requests
from flask import Flask, session, render_template, redirect, url_for, request
import os

app = Flask(__name__)


app.secret_key = os.environ['secret_key']


@app.route('/')
def location():
    if (session and session['ip_info']):
        data = session['ip_info']
        return redirect(
            url_for('weather', city=data['city'], state=data['state'])
        )
    else:
        data = get_ip_info()
        if data['success']:
            session['ip_info'] = data
            return redirect(
                url_for('weather', city=data['city'], state=data['state'])
            )
        else:
            return redirect(url_for('error_page'))


def celsius():
    if hasattr(os.environ, "celsius"):
        if os.environ['celsius']:
            return "?units=si"

    return ""


@app.route('/weather/<city>/<state>')
def weather(city, state):
    weather_key = os.environ['weather_key']

    if 'ip_info' in session:
        data = session['ip_info']
        geo_info = data['ip_coords']
    else:
        geo_info = get_geo_info(city, state)

    if geo_info is None:
        return error_page('GEO info Missing!')
    
    # request weather info from the weather API
    # format for weather api request =
    # https://api.darksky.net/forecast/[key]/[latitude],[longitude]
    response = requests.get(
        'https://api.forecast.io/forecast/%s/%s%s' % (
            weather_key, geo_info, celsius()
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

    # print out a statement with the current weather info + location that was
    # used/detected
    # return("Right now in "+ city + ", " + state + " it is " + temperature
    # + degree_sign + " and there is a " + RAIN_WARNING)
    location = {'city': city, 'state': state}

    weather_info = {'temperature': temperature, 'rain': rain_commentary}
    return render_template(
        'weather.html',
        location=location,
        weather_info=weather_info,
        weather_icon=weather_icon
    )

@app.errorhandler(404)
def error_page(error):
    return render_template('404.html'), 404


# private non-route methods
def get_ip_info():

    if 'X-Forwarded-For' in request.headers:
        user_ip = str(request.headers['X-Forwarded-For'])
    else:
        user_ip = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))


    # do not use local host ip address as the user_ip
    if user_ip == '127.0.0.1':
        user_ip = requests.get('http://ip.42.pl/raw').text

 
    # get location information based off of IP address
    url = 'http://ip-api.com/json/' + user_ip
    response = requests.get(url)
    js = response.json()

    return {
        'success': js['status'] == 'success',
        'city': js['city'],
        'state': js['regionName'],
        'ip_coords': get_geo_str(js['lat'], js['lon'])
    }

def get_geo_info(city, state):
    # get location information based off of city/state
    url = 'http://www.datasciencetoolkit.org/maps/api/geocode/json?sensor=false&address=%s,%s' % (city, state)
    response = requests.get(url)
    js = response.json()

    if js['status'] == 'OK':
        lat = js['results'][0]['geometry']['location']['lat']
        lon = js['results'][0]['geometry']['location']['lng']
        return get_geo_str(lat, lon)
    else:
        return None;

def get_geo_str(lat, lon):
    return str(lat) + "," + str(lon)

if __name__ == '__main__':
    app.run()
