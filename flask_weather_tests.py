# TODO: rename this file and class if changing the app name

import app as fw

import unittest

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

if __name__ == '__main__':
    unittest.main()
