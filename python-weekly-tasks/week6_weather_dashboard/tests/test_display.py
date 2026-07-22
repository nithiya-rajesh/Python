"""
test_display.py
Unit tests for weather_app.weather_display - ensures rendered output
contains the expected data without crashing, regardless of color support.
"""

import unittest

from weather_app import weather_display as display


class TestRenderCurrentWeather(unittest.TestCase):
    def setUp(self):
        self.sample_current = {
            "city": "London",
            "country": "GB",
            "temperature": 8,
            "feels_like": 5,
            "temp_min": 6,
            "temp_max": 10,
            "unit_symbol": "°C",
            "condition": "Rain",
            "description": "Light Rain",
            "icon": "🌧️",
            "humidity": 87,
            "pressure": 1009,
            "wind_speed": 22,
            "wind_unit": "km/h",
            "wind_deg": 200,
            "visibility_km": 8.0,
            "sunrise": "07:45",
            "sunset": "16:30",
            "last_updated": "2024-01-25 10:15:00",
            "cache_age_seconds": 0,
        }

    def test_contains_city_and_temperature(self):
        output = display.render_current_weather(self.sample_current)
        self.assertIn("London", output)
        self.assertIn("8", output)
        self.assertIn("Light Rain", output)

    def test_cache_note_appears_when_cached(self):
        cached = dict(self.sample_current)
        cached["cache_age_seconds"] = 300
        output = display.render_current_weather(cached)
        self.assertIn("cached data", output)


class TestRenderForecast(unittest.TestCase):
    def test_renders_each_day(self):
        forecast = [
            {
                "date": "Thu 25 Jan",
                "temp_max": 9,
                "temp_min": 6,
                "unit_symbol": "°C",
                "humidity_avg": 85,
                "condition": "Rain",
                "description": "Light Rain",
                "icon": "🌧️",
            },
            {
                "date": "Fri 26 Jan",
                "temp_max": 8,
                "temp_min": 4,
                "unit_symbol": "°C",
                "humidity_avg": 78,
                "condition": "Clouds",
                "description": "Overcast",
                "icon": "☁️",
            },
        ]
        output = display.render_forecast(forecast)
        self.assertIn("Thu 25 Jan", output)
        self.assertIn("Fri 26 Jan", output)

    def test_empty_forecast_message(self):
        output = display.render_forecast([])
        self.assertIn("No forecast data", output)


class TestRenderHelpers(unittest.TestCase):
    def test_render_help_lists_commands(self):
        output = display.render_help()
        self.assertIn("search", output)
        self.assertIn("units", output)
        self.assertIn("quit", output)

    def test_render_error_includes_message(self):
        output = display.render_error("City not found")
        self.assertIn("City not found", output)

    def test_render_favorites_empty(self):
        output = display.render_favorites([])
        self.assertIn("No favorite cities", output)

    def test_render_favorites_with_entries(self):
        output = display.render_favorites([{"city": "Tokyo", "country": "JP"}])
        self.assertIn("Tokyo", output)


if __name__ == "__main__":
    unittest.main()
