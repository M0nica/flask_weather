# flask_weather

Flask app to auto-detect local weather (temperature and chance of rain) based off of user's IP address.

<img src="https://raw.githubusercontent.com/M0nica/flask_weather/master/static/nyc_weather_screenshot.png">

*Example screenshot of flask_weather application*

## Setup

- Install dependencies
 - `pip install -r requirements.txt`
- Add `config.py`
  - Setup config.py with the line `weather_key = "###############";`. The weather_key is the API key received from registering at https://darksky.net/dev.
- Run  
  - `python app.py` 

## Functionality

Get a user's IP address and then used http://ip-api.com/ to get more specific location information to pass into Weather API (https://darksky.net/dev/). Weather information (current temperature and % chance of rain) is returned based on the location associated with the IP.

To work on this locally clone the repo, request and add an API key (locally) from darksky and then run `app.py`



`weather.html` displays the weather information and displays appropriate weather icon (https://erikflowers.github.io/weather-icons/) based on what the current weather is.

## Sample Output:

### Today's Weather Forecast for Brooklyn, New York
Right now it is 41° and there is a 0% chance of rain.

### Today's Weather Forecast for City, State
Right now it is X° and there is a Y% chance of rain.
