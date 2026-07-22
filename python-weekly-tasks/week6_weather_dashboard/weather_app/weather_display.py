"""
weather_display.py
Formats parsed weather data into a readable, color-coded command-line
display: current conditions, 5-day forecast, help text, and favorites list.
"""

from typing import Dict, List

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

    class _NoColor:
        def __getattr__(self, _name):
            return ""

    Fore = _NoColor()
    Style = _NoColor()


def _temp_color(temp: float, units: str = "metric") -> str:
    """Return a color code based on how hot/cold the temperature is."""
    if not COLOR_ENABLED:
        return ""
    threshold = temp if units == "metric" else (temp - 32) * 5 / 9  # normalize to C
    if threshold <= 0:
        return Fore.CYAN
    if threshold <= 15:
        return Fore.BLUE
    if threshold <= 25:
        return Fore.GREEN
    if threshold <= 32:
        return Fore.YELLOW
    return Fore.RED


def _reset() -> str:
    return Style.RESET_ALL if COLOR_ENABLED else ""


def render_header(title: str = "WEATHER DASHBOARD") -> str:
    bar = "=" * (len(title) + 4)
    return f"\n🌤️  {title}\n{bar}\n"


def render_current_weather(data: Dict, units: str = "metric") -> str:
    """Render the current weather block."""
    color = _temp_color(data["temperature"], units)
    reset = _reset()
    cache_note = ""
    if data.get("cache_age_seconds", 0) > 0:
        minutes = data["cache_age_seconds"] // 60
        cache_note = f"\nAPI Status: Using cached data ({minutes} minute(s) old)"

    lines = [
        f"📍 Current Location: {data['city']}, {data['country']}",
        f"🕐 Last Updated: {data['last_updated']}",
        "",
        "Current Weather:",
        "─" * 16,
        (
            f"Temperature:   {color}{data['temperature']}{data['unit_symbol']}{reset} "
            f"(Feels like: {data['feels_like']}{data['unit_symbol']})"
        ),
        f"Conditions:    {data['description']} {data['icon']}",
        f"Humidity:      {data['humidity']}%",
        f"Wind:          {data['wind_speed']} {data['wind_unit']}",
        f"Pressure:      {data['pressure']} hPa",
        f"Visibility:    {data['visibility_km']} km",
        f"Sunrise:       {data['sunrise']}",
        f"Sunset:        {data['sunset']}",
        cache_note,
    ]
    return "\n".join(line for line in lines if line is not None)


def render_forecast(forecast_days: List[Dict], units: str = "metric") -> str:
    """Render the multi-day forecast block."""
    if not forecast_days:
        return "No forecast data available."

    lines = [
        "",
        f"{len(forecast_days)}-Day Forecast:",
        "─" * 16,
    ]
    for day in forecast_days:
        high_color = _temp_color(day["temp_max"], units)
        low_color = _temp_color(day["temp_min"], units)
        reset = _reset()
        lines.append(
            f"{day['date']:<11} {day['icon']}  "
            f"{high_color}{day['temp_max']}{day['unit_symbol']}{reset} / "
            f"{low_color}{day['temp_min']}{day['unit_symbol']}{reset}  "
            f"(Humidity: {day['humidity_avg']}%)  {day['description']}"
        )
    return "\n".join(lines)


def render_search_results(results: List[Dict]) -> str:
    if not results:
        return "No matching cities found."
    lines = ["", "Search Results:", "─" * 15]
    for i, r in enumerate(results, 1):
        lines.append(f"  {i}. {r['label']}")
    return "\n".join(lines)


def render_favorites(favorites: List[Dict]) -> str:
    if not favorites:
        return "No favorite cities saved yet. Use 'fav add <city>' to add one."
    lines = ["", "⭐ Favorite Cities:", "─" * 18]
    for i, fav in enumerate(favorites, 1):
        lines.append(f"  {i}. {fav['city']}" + (f", {fav['country']}" if fav.get("country") else ""))
    return "\n".join(lines)


def render_help() -> str:
    return """
Available Commands:
────────────────────
<city name>          Show current weather + forecast for a city
search <query>        Search/autocomplete cities by name
units                 Toggle between Celsius and Fahrenheit
fav add <city>        Add a city to favorites
fav remove <city>     Remove a city from favorites
fav list              List all favorite cities
export <city>         Export current weather + forecast data to CSV
refresh               Force-refresh data (bypass cache) for the last city
help                  Show this help message
quit / exit           Exit the application
"""


def render_error(message: str) -> str:
    color = Fore.RED if COLOR_ENABLED else ""
    reset = _reset()
    return f"{color}❌ Error: {message}{reset}"


def render_info(message: str) -> str:
    color = Fore.CYAN if COLOR_ENABLED else ""
    reset = _reset()
    return f"{color}ℹ️  {message}{reset}"
