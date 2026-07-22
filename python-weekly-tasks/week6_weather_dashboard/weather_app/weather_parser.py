"""
weather_parser.py
Parses raw OpenWeatherMap JSON responses into clean, display-ready data
structures. Handles unit conversion, date/time formatting, and weather
condition -> icon mapping.
"""

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List

# Maps OpenWeatherMap's main condition groups to emoji icons.
CONDITION_ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️",
    "Smoke": "🌫️",
    "Dust": "🌪️",
    "Sand": "🌪️",
    "Ash": "🌋",
    "Squall": "💨",
    "Tornado": "🌪️",
}

DEFAULT_ICON = "🌡️"


def get_icon(condition_main: str) -> str:
    """Return an emoji icon for a given weather condition group."""
    return CONDITION_ICONS.get(condition_main, DEFAULT_ICON)


def celsius_to_fahrenheit(celsius: float) -> float:
    return round((celsius * 9 / 5) + 32, 1)


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return round((fahrenheit - 32) * 5 / 9, 1)


def format_unix_time(unix_ts: int, tz_offset_seconds: int = 0, fmt: str = "%H:%M") -> str:
    """Convert a UNIX timestamp (UTC) to a local, formatted time string."""
    local_dt = datetime.fromtimestamp(unix_ts + tz_offset_seconds, tz=timezone.utc)
    return local_dt.strftime(fmt)


def parse_current_weather(raw: Dict[str, Any], units: str = "metric") -> Dict[str, Any]:
    """Turn a raw /weather API response into a clean dict for display."""
    weather = raw.get("weather", [{}])[0]
    main = raw.get("main", {})
    wind = raw.get("wind", {})
    sys = raw.get("sys", {})
    tz_offset = raw.get("timezone", 0)

    unit_symbol = "°C" if units == "metric" else "°F"
    speed_unit = "km/h" if units == "metric" else "mph"
    wind_speed = wind.get("speed", 0)
    if units == "metric":
        wind_speed = round(wind_speed * 3.6, 1)  # m/s -> km/h
    else:
        wind_speed = round(wind_speed, 1)  # already mph from API

    return {
        "city": raw.get("name", "Unknown"),
        "country": sys.get("country", ""),
        "temperature": round(main.get("temp", 0)),
        "feels_like": round(main.get("feels_like", 0)),
        "temp_min": round(main.get("temp_min", 0)),
        "temp_max": round(main.get("temp_max", 0)),
        "unit_symbol": unit_symbol,
        "condition": weather.get("main", "Unknown"),
        "description": weather.get("description", "").title(),
        "icon": get_icon(weather.get("main", "")),
        "humidity": main.get("humidity", 0),
        "pressure": main.get("pressure", 0),
        "wind_speed": wind_speed,
        "wind_unit": speed_unit,
        "wind_deg": wind.get("deg", 0),
        "visibility_km": round(raw.get("visibility", 0) / 1000, 1),
        "sunrise": format_unix_time(sys.get("sunrise", 0), tz_offset),
        "sunset": format_unix_time(sys.get("sunset", 0), tz_offset),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cache_age_seconds": raw.get("_cache_age_seconds", 0),
    }


def parse_forecast(raw: Dict[str, Any], units: str = "metric") -> List[Dict[str, Any]]:
    """
    Turn a raw /forecast API response (3-hour intervals) into a list of
    daily summaries with min/max temperature and dominant condition.
    """
    unit_symbol = "°C" if units == "metric" else "°F"
    tz_offset = raw.get("city", {}).get("timezone", 0)
    entries = raw.get("list", [])

    daily_buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        dt = datetime.fromtimestamp(entry["dt"] + tz_offset, tz=timezone.utc)
        day_key = dt.strftime("%Y-%m-%d")
        daily_buckets[day_key].append(entry)

    daily_summaries = []
    for day_key, day_entries in sorted(daily_buckets.items())[:5]:
        temps = [e["main"]["temp"] for e in day_entries]
        humidities = [e["main"]["humidity"] for e in day_entries]

        # Use the entry closest to midday as the "representative" condition
        midday_entry = min(
            day_entries,
            key=lambda e: abs(
                datetime.fromtimestamp(e["dt"] + tz_offset, tz=timezone.utc).hour - 12
            ),
        )
        condition_main = midday_entry["weather"][0]["main"]
        description = midday_entry["weather"][0]["description"].title()

        day_date = datetime.strptime(day_key, "%Y-%m-%d")

        daily_summaries.append(
            {
                "date": day_date.strftime("%a %d %b"),
                "temp_max": round(max(temps)),
                "temp_min": round(min(temps)),
                "unit_symbol": unit_symbol,
                "humidity_avg": round(sum(humidities) / len(humidities)),
                "condition": condition_main,
                "description": description,
                "icon": get_icon(condition_main),
            }
        )

    return daily_summaries


def parse_city_search_results(raw: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Normalize geocoding search results for autocomplete display."""
    results = []
    for entry in raw:
        name = entry.get("name", "")
        state = entry.get("state", "")
        country = entry.get("country", "")
        label_parts = [p for p in (name, state, country) if p]
        results.append(
            {
                "name": name,
                "country": country,
                "state": state,
                "label": ", ".join(label_parts),
            }
        )
    return results
