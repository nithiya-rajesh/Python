"""
test_parser.py
Unit tests for weather_app.weather_parser - unit conversions, icon mapping,
and JSON-to-display parsing.
"""

import unittest

from weather_app.weather_parser import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    get_icon,
    parse_city_search_results,
    parse_current_weather,
    parse_forecast,
)


class TestUnitConversion(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32)
        self.assertEqual(celsius_to_fahrenheit(100), 212)

    def test_fahrenheit_to_celsius(self):
        self.assertEqual(fahrenheit_to_celsius(32), 0)
        self.assertEqual(fahrenheit_to_celsius(212), 100)


class TestIconMapping(unittest.TestCase):
    def test_known_condition(self):
        self.assertEqual(get_icon("Clear"), "☀️")
        self.assertEqual(get_icon("Rain"), "🌧️")

    def test_unknown_condition_returns_default(self):
        self.assertEqual(get_icon("SomethingWeird"), "🌡️")


class TestParseCurrentWeather(unittest.TestCase):
    def test_parses_expected_fields(self):
        raw = {
            "name": "London",
            "sys": {"country": "GB", "sunrise": 1700000000, "sunset": 1700030000},
            "main": {
                "temp": 10.4,
                "feels_like": 8.1,
                "temp_min": 8,
                "temp_max": 12,
                "humidity": 87,
                "pressure": 1009,
            },
            "weather": [{"main": "Rain", "description": "light rain"}],
            "wind": {"speed": 6.1, "deg": 200},
            "visibility": 8000,
            "timezone": 0,
        }
        parsed = parse_current_weather(raw, units="metric")

        self.assertEqual(parsed["city"], "London")
        self.assertEqual(parsed["country"], "GB")
        self.assertEqual(parsed["temperature"], 10)
        self.assertEqual(parsed["condition"], "Rain")
        self.assertEqual(parsed["description"], "Light Rain")
        self.assertEqual(parsed["visibility_km"], 8.0)
        self.assertIn("humidity", parsed)


class TestParseForecast(unittest.TestCase):
    def test_groups_entries_by_day(self):
        raw = {
            "city": {"timezone": 0},
            "list": [
                {
                    "dt": 1700000000 + i * 3600 * 3,
                    "main": {"temp": 10 + i, "humidity": 70},
                    "weather": [{"main": "Clouds", "description": "few clouds"}],
                }
                for i in range(16)  # ~2 days of 3-hour intervals
            ],
        }
        forecast = parse_forecast(raw, units="metric")
        self.assertGreaterEqual(len(forecast), 1)
        self.assertIn("temp_max", forecast[0])
        self.assertIn("temp_min", forecast[0])
        self.assertIn("icon", forecast[0])


class TestParseCitySearchResults(unittest.TestCase):
    def test_builds_readable_labels(self):
        raw = [{"name": "Paris", "state": "", "country": "FR"}]
        results = parse_city_search_results(raw)
        self.assertEqual(results[0]["label"], "Paris, FR")


if __name__ == "__main__":
    unittest.main()
