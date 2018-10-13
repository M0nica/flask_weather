# Flask Weather App ☀️☔️

This is a Flask (Python) application that auto-detects local weather based off of user's external IP address.

<img src="https://raw.githubusercontent.com/M0nica/flask_weather/master/static/nyc_weather_screenshot.png">

_Example screenshot of flask_weather application_

## Setup

- Install dependencies
- `pip install -r requirements.txt`
- Add environment variables
  - `weather_key="###############";`. The weather_key is the API key received from registering at https://darksky.net/dev.
  - add `secret_key="********"`. It should be a random string that is hard to guess.
- Run
  - `python app.py`
- Run Tests
  - `python flask_weather_tests.py`

## Functionality

Gets a user's external IP address and then used http://freegeoip.net to get more specific location information to pass into Weather API (https://darksky.net/dev/). Weather information (current temperature and % chance of rain) is returned based on the location associated with the IP.

To work on this locally clone the repo, request and add an API key (locally) from darksky and then run `app.py`

`weather.html` displays the weather information and displays appropriate weather icon (https://erikflowers.github.io/weather-icons/) based on what the current weather is.

To display temperature in Celsius instead of Fahrenheit, set `celsius = True` environment variables.

## Sample Output:

### Today's Weather Forecast for Brooklyn, New York

Right now it is 41° and there is a 0% chance of rain.

### Today's Weather Forecast for City, State

Right now it is X° and there is a Y% chance of rain.
