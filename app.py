import requests
from flask import Flask, session, render_template, redirect, url_for
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
    # degree_sign = u'\N{DEGREE SIGN}'

    data = session['ip_info']
    # request weather info from the weather API
    # format for weather api request =
    # https://api.darksky.net/forecast/[key]/[latitude],[longitude]
    response = requests.get(
        'https://api.forecast.io/forecast/%s/%s%s' % (
            weather_key, data['ip_coords'], celsius()
        )
    )
    data = response.json()

    # data['hourly'] contains hourly data with the time formatted as Epoch
    # Unix Time - should look into how to display hourly data in weather.html
    # data['hourly']

    weather_icon = str(data['currently']['icon'])
    temperature = str(int(data['currently']['temperature']))
    RAIN_WARNING = data['daily']['data'][0]['precipProbability']

    rain_level = {
                    0:  "there is a slight chance of rain. " \
                        "You might want to grab an umbrella ☔",
                    1:  "there is a high chance of rain. " \
                        "Grab an umbrella on your way out! ☔",
                    2:  "it is raining right now!",
                    3:  "it is definitely going to rain today! " \
                        "GRAB YOUR UMBRELLA. ☔"
                }

    if RAIN_WARNING == 0:
        rain_commentary = weather_commentary(temperature)
    elif 0 < RAIN_WARNING <= .5:
        rain_commentary = rain_level[0]
    elif .5 < RAIN_WARNING < .75:
        rain_commentary = rain_level[1]
    elif RAIN_WARNING == 1:
        rain_commentary = rain_level[2]
    else:
        rain_commentary = rain_level[3]
    

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
    ip = requests.get('http://ip.42.pl/raw').text
    r = requests.get('http://ip-api.com/json/#' + ip)
    js = r.json()

    return {
        'success': js['status'] == 'success',
        'city': js['city'],
        'state': js['regionName'],
        'ip_coords': str(js['lat']) + ", " + str(js['lon'])
    }

def weather_commentary(temperature):
    temperature = int(temperature)
    temperature_level = {
                0:  "it's scorching hot. Stay cool!",
                1:  "it's hot and sunny. Don't forget that sunscreen!",
                2:  "it's nice and warm today. Time to flex those flip-flops",
                3:  "a cup of hot cappucino would be nice on this cool weather",
                4:  "it's gonna be cold today. Make sure you keep yourself warm!",
                5:  "winter is here! Brrrrrrr",
                6:  "it's Freezing Cold."
    }

    if temperature >= 95:
        return temperature_level[0]
    elif 80 <= temperature <= 94:
        return temperature_level[1]
    elif 69 <= temperature <= 79:
        return temperature_level[2]
    elif 59 <= temperature <= 68:
        return temperature_level[3]
    elif 40 <= temperature <= 57:
        return temperature_level[4]
    elif 25 <= temperature <= 39:
        return temperature_level[5]
    elif temperature <= 24:
        return temperature_level[6]

if __name__ == '__main__':
    app.run()
