# TODO: rename this file and class if changing the app name

import app as fw

import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

class FlaskWeatherTestCase(unittest.TestCase):

    # runs before each test
    def setUp(self):
        fw.app.testing = True
        self.app = fw.app.test_client()

    def test_default_route_returns_success(self):
        request = self.app.get('/')
        # this will be a 302 since the default route redirects
        self.assertEqual(302, request.status_code)

    def test_invalid_route_returns_404_page(self):
        request = self.app.get('/doesnotexist')
        self.assertEqual(404, request.status_code)

    @patch('app.get_weather_data', return_value=('partly-cloudy-day', 37, 0))
    def test_correct_weather_is_displayed_partly_cloudy(self, get_weather_data):
        request = self.app.get('/weather/Stockholm/Stockholm')
        self.assertEqual(200, request.status_code)
        soup = BeautifulSoup(request.data, features="html5lib")
        weatherLocation = soup.select('.weather-container > h1')[0].getText()
        self.assertEqual('Stockholm, Stockholm', weatherLocation)
        weatherText = soup.find('span', {'class': 'weather-degrees'}).string
        self.assertIn('37', weatherText)
        weatherDetailedText = soup.select('.weather-container > p')[0].getText()
        self.assertIn('Right now it is 37', weatherDetailedText)
        self.assertIn('there is a no chance of rain! It\'s a sunny day', weatherDetailedText)
        weatherIcon = soup.find('i', {'class': 'wi-forecast-io-partly-cloudy-day'})
        self.assertTrue(weatherIcon)

    @patch('app.get_weather_data', return_value=('rain', 32, 0.3))
    def test_correct_weather_is_displayed_chance_of_rain(self, get_weather_data):
        request = self.app.get('/weather/Stockholm/Stockholm')
        self.assertEqual(200, request.status_code)
        soup = BeautifulSoup(request.data, features="html5lib")
        weatherLocation = soup.select('.weather-container > h1')[0].getText()
        self.assertEqual('Stockholm, Stockholm', weatherLocation)
        weatherText = soup.find('span', {'class': 'weather-degrees'}).string
        self.assertIn('32', weatherText)
        weatherDetailedText = soup.select('.weather-container > p')[0].getText()
        self.assertIn('Right now it is 32', weatherDetailedText)
        self.assertIn("there is a slight chance of rain", weatherDetailedText)
        weatherIcon = soup.find('i', {'class': 'wi-rain'})
        self.assertTrue(weatherIcon)

if __name__ == '__main__':
    unittest.main()
    
