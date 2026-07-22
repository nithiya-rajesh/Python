"""
test_api.py
Unit tests for weather_app.weather_api.WeatherAPI using mocked HTTP requests
so tests run without real network access or an API key.
"""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from weather_app.weather_api import WeatherAPI, WeatherAPIError


class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.api = WeatherAPI(api_key="test_key", base_url="https://fake.api")
        self.api.cache_dir = Path(self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    @patch("weather_app.weather_api.requests.get")
    def test_get_current_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "London",
            "sys": {"country": "GB"},
            "main": {"temp": 10, "feels_like": 8, "humidity": 80, "pressure": 1010},
            "weather": [{"main": "Rain", "description": "light rain"}],
            "wind": {"speed": 5},
        }
        mock_get.return_value = mock_response

        data = self.api.get_current_weather("London")
        self.assertEqual(data["name"], "London")
        mock_get.assert_called_once()

    @patch("weather_app.weather_api.requests.get")
    def test_get_current_weather_invalid_key(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with self.assertRaises(WeatherAPIError):
            self.api.get_current_weather("London")

    @patch("weather_app.weather_api.requests.get")
    def test_get_current_weather_city_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(WeatherAPIError):
            self.api.get_current_weather("NotARealCity123")

    @patch("weather_app.weather_api.requests.get")
    def test_caching_avoids_second_request(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Paris",
            "sys": {"country": "FR"},
            "main": {"temp": 15, "feels_like": 14, "humidity": 60, "pressure": 1015},
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "wind": {"speed": 3},
        }
        mock_get.return_value = mock_response

        self.api.get_current_weather("Paris")
        self.api.get_current_weather("Paris")  # should be served from cache

        self.assertEqual(mock_get.call_count, 1)

    @patch("weather_app.weather_api.requests.get")
    def test_rate_limit_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        with self.assertRaises(WeatherAPIError):
            self.api.get_current_weather("Berlin")


if __name__ == "__main__":
    unittest.main()
