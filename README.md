# flask_weather

Flask app to auto-detect local weather (temperature and chance of rain) based off of user's IP address.

## Setup

- Install dependencies
 - `pip install -r requirements.txt`
- Add `config.py`
  - Setup config.py with the line `weather_key = "###############";`. The weather_key is the API key received from registering at https://darksky.net/dev.
- Run  
  - `python app.py` 

## Functionality

Uses ipgetter to get a user's IP address and then used http://freegeoip.net to get more specific location information to pass into Weather API (https://darksky.net/dev/). Weather information (current temperature and % chance of rain) is returned based on the location associated with the IP.



`weather.html` displays the weather information and displays appropriate weather icon (https://erikflowers.github.io/weather-icons/) based on what the current weather is.

##Sample Output:

### Today's Weather Forecast for Brooklyn, New York
Right now it is 41° and there is a 0% chance of rain.

### Today's Weather Forecast for City, State
Right now it is X° and there is a Y% chance of rain.
