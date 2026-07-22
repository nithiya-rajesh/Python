"""
weather_api.py
Handles all communication with the OpenWeatherMap API: current weather,
5-day forecast, and city geocoding/search - with request caching and
robust error handling.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from .config import Config


class WeatherAPIError(Exception):
    """Raised when the weather API returns an unrecoverable error."""


class WeatherAPI:
    """Handles all weather API interactions."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        units: str = "metric",
    ):
        self.api_key = api_key or Config.API_KEY
        self.base_url = base_url or Config.BASE_URL
        self.geocode_url = Config.GEOCODE_URL
        self.units = units  # 'metric' or 'imperial'
        self.cache_dir: Path = Config.CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_duration = Config.CACHE_DURATION

    # ------------------------------------------------------------------ #
    # Caching helpers
    # ------------------------------------------------------------------ #
    def _cache_path(self, cache_key: str) -> Path:
        safe_key = cache_key.replace(" ", "_").replace(",", "_").lower()
        return self.cache_dir / f"{safe_key}.json"

    def _get_cached_data(self, cache_key: str) -> Optional[Dict]:
        """Return cached data if it exists and hasn't expired."""
        cache_file = self._cache_path(cache_key)
        if cache_file.exists():
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < self.cache_duration:
                try:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        payload = json.load(f)
                        payload["_cache_age_seconds"] = int(cache_age)
                        return payload
                except (json.JSONDecodeError, OSError):
                    return None
        return None

    def _save_to_cache(self, cache_key: str, data: Dict) -> None:
        cache_file = self._cache_path(cache_key)
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError:
            pass  # Caching is best-effort; don't crash the app over it

    def clear_cache(self) -> int:
        """Delete all cached files. Returns number of files removed."""
        count = 0
        for file in self.cache_dir.glob("*.json"):
            file.unlink(missing_ok=True)
            count += 1
        return count

    # ------------------------------------------------------------------ #
    # Core request handler
    # ------------------------------------------------------------------ #
    def _make_request(self, url: str, params: Dict[str, Any]) -> Optional[Any]:
        """Make an API request with consistent error handling."""
        try:
            params = dict(params)
            params["appid"] = self.api_key
            response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)

            if response.status_code == 200:
                return response.json()
            if response.status_code == 401:
                raise WeatherAPIError(
                    "Invalid API key. Check your .env file / OPENWEATHER_API_KEY."
                )
            if response.status_code == 404:
                raise WeatherAPIError("City not found. Check the spelling and try again.")
            if response.status_code == 429:
                raise WeatherAPIError("API rate limit exceeded. Please wait and try again.")

            raise WeatherAPIError(
                f"API request failed with status {response.status_code}: {response.text[:200]}"
            )

        except requests.exceptions.Timeout as exc:
            raise WeatherAPIError("Request timed out. Check your internet connection.") from exc
        except requests.exceptions.ConnectionError as exc:
            raise WeatherAPIError("Network connection error. Are you online?") from exc
        except requests.exceptions.RequestException as exc:
            raise WeatherAPIError(f"Unexpected network error: {exc}") from exc

    # ------------------------------------------------------------------ #
    # Public API methods
    # ------------------------------------------------------------------ #
    def get_current_weather(self, city: str, country_code: Optional[str] = None) -> Dict:
        """Get current weather for a city (uses cache when available)."""
        query = f"{city},{country_code}" if country_code else city
        cache_key = f"current_{query}_{self.units}"

        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        params = {"q": query, "units": self.units}
        data = self._make_request(f"{self.base_url}/weather", params)
        self._save_to_cache(cache_key, data)
        data["_cache_age_seconds"] = 0
        return data

    def get_forecast(self, city: str, country_code: Optional[str] = None, days: int = 5) -> Dict:
        """Get a multi-day forecast for a city (3-hour interval data from OWM)."""
        query = f"{city},{country_code}" if country_code else city
        cache_key = f"forecast_{query}_{self.units}"

        cached = self._get_cached_data(cache_key)
        if cached:
            return cached

        params = {"q": query, "units": self.units, "cnt": days * 8}
        data = self._make_request(f"{self.base_url}/forecast", params)
        self._save_to_cache(cache_key, data)
        data["_cache_age_seconds"] = 0
        return data

    def search_cities(self, query: str, limit: int = 5) -> List[Dict]:
        """Search/autocomplete cities by name using the geocoding endpoint."""
        if not query or len(query.strip()) < 2:
            return []

        cache_key = f"search_{query.strip()}"
        cached = self._get_cached_data(cache_key)
        if cached and isinstance(cached.get("results"), list):
            return cached["results"]

        params = {"q": query, "limit": limit}
        data = self._make_request(f"{self.geocode_url}/direct", params)
        results = data if isinstance(data, list) else []
        self._save_to_cache(cache_key, {"results": results})
        return results

    def get_weather_by_ip(self) -> Optional[Dict]:
        """Best-effort location detection using a free IP geolocation service."""
        try:
            resp = requests.get("https://ipapi.co/json/", timeout=Config.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                info = resp.json()
                city = info.get("city")
                if city:
                    return self.get_current_weather(city, info.get("country_code"))
        except requests.exceptions.RequestException:
            return None
        return None
