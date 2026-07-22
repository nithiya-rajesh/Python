# 🌤️ Weather Dashboard Application

**Week 6 Project — Working with External Libraries**

A comprehensive command-line weather application that fetches real-time weather
data, forecasts, and location search results from the OpenWeatherMap API and
displays them in a friendly, color-coded terminal interface. This project
demonstrates API integration, external library usage, caching, and
professional Python development practices.

---

## Project Description

The Weather Dashboard lets you look up the current weather and 5-day forecast
for any city in the world, search for cities by name, save favorites, switch
between Celsius and Fahrenheit, and export weather data to CSV — all from an
interactive command-line menu.

## What I Learned

- **API Integration:** How to work with external web services (OpenWeatherMap)
- **HTTP Requests:** Making GET requests and handling responses with `requests`
- **JSON Processing:** Parsing and working with complex, nested JSON data
- **Error Handling:** Managing network errors, timeouts, and API-specific failures (401/404/429)
- **Environment Management:** Using `.env` files and environment variables for configuration/secrets
- **Package Management:** Installing and managing dependencies with `pip` and `requirements.txt`
- **Caching:** Reducing redundant API calls with a simple file-based cache
- **Modular Design:** Splitting a CLI app into API, parsing, display, and controller layers

## Features

- ✅ Current weather for any city worldwide
- ✅ 5-day weather forecast with daily summaries
- ✅ Temperature in Celsius or Fahrenheit (toggle anytime)
- ✅ Weather condition icons and descriptions
- ✅ Wind speed, humidity, pressure, and visibility details
- ✅ City search / autocomplete via geocoding API
- ✅ Favorite cities management (add / remove / list, persisted to JSON)
- ✅ API response caching (10-minute default, configurable)
- ✅ Comprehensive error handling (invalid key, city not found, rate limit, network errors)
- ✅ Export current + forecast weather data to CSV
- ✅ Color-coded temperature display (via `colorama`, optional)

## Project Structure

```
week6-weather-dashboard/
│── weather_app/
│   ├── __init__.py
│   ├── config.py            # Environment variables & app settings
│   ├── weather_api.py       # API client: current weather, forecast, city search, caching
│   ├── weather_parser.py    # JSON → clean data, unit conversion, icons, date formatting
│   ├── weather_display.py   # Terminal rendering: current weather, forecast, help, errors
│   └── main.py              # Interactive CLI menu / application entry point
│── data/
│   ├── cache/                # Cached API responses (auto-created, gitignored)
│   ├── exports/               # CSV exports (auto-created, gitignored)
│   └── favorites.json        # Saved favorite cities
│── tests/
│   ├── __init__.py
│   ├── test_api.py           # Mocked tests for WeatherAPI
│   ├── test_parser.py        # Tests for parsing & unit conversion
│   └── test_display.py       # Tests for terminal rendering
│── requirements.txt
│── .env.example
│── README.md
└── .gitignore
```

## How to Run

1. **Get an API key** from [OpenWeatherMap](https://openweathermap.org/api) (free tier is sufficient).
2. **Copy the environment template** and add your key:
   ```bash
   cp .env.example .env
   # then edit .env and set OPENWEATHER_API_KEY=your_actual_key
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app:**
   ```bash
   python -m weather_app.main
   ```

> 💡 It can take a few minutes after signing up for a new OpenWeatherMap key to activate.

## Required Libraries

| Library | Purpose |
|---|---|
| `requests` | Making HTTP requests to the weather and geocoding APIs |
| `python-dotenv` | Loading API keys and settings from a `.env` file |
| `colorama` | Color-coded terminal output (optional — app works without it) |

## Usage / Commands

Once running, type a city name to see its weather, or use one of these commands:

| Command | Description |
|---|---|
| `<city name>` | Show current weather + 5-day forecast for a city |
| `search <query>` | Search / autocomplete cities by name |
| `units` | Toggle between Celsius and Fahrenheit |
| `fav add <city>` | Add a city to favorites |
| `fav remove <city>` | Remove a city from favorites |
| `fav list` | List all favorite cities |
| `export <city>` | Export current weather + forecast to a CSV file |
| `refresh` | Force-refresh data (bypass cache) for the last city checked |
| `help` | Show the command list |
| `quit` / `exit` | Exit the application |

## Sample Output

```
🌤️  WEATHER DASHBOARD
=======================

📍 Current Location: London, GB
🕐 Last Updated: 2024-01-25 10:15:00

Current Weather:
────────────────
Temperature:   8°C (Feels like: 5°C)
Conditions:    Light Rain 🌧️
Humidity:      87%
Wind:          22 km/h
Pressure:      1009 hPa
Visibility:    8.0 km
Sunrise:       07:45
Sunset:        16:30

5-Day Forecast:
───────────────
Thu 25 Jan  🌧️  9°C / 6°C   (Humidity: 85%)  Light Rain
Fri 26 Jan  ☁️  8°C / 4°C   (Humidity: 78%)  Overcast Clouds
Sat 27 Jan  ⛅  7°C / 3°C   (Humidity: 75%)  Scattered Clouds
Sun 28 Jan  ☀️  9°C / 4°C   (Humidity: 70%)  Clear Sky
Mon 29 Jan  ☀️ 10°C / 5°C   (Humidity: 68%)  Clear Sky

Type a city name to check the weather, or 'help' for commands.
```

## Running Tests

Tests use mocked HTTP requests, so no API key or network access is required.

```bash
python -m unittest discover tests
```

or, if you have `pytest` installed:

```bash
pytest tests/
```

## Technical Notes

- **Caching:** Responses are cached to disk in `data/cache/` for 10 minutes by
  default (`CACHE_DURATION` in `.env`), keyed by city + unit system, to reduce
  API calls and respect rate limits.
- **Error Handling:** All API failures (invalid key, city not found, rate
  limiting, timeouts, connection errors) are caught and surfaced as friendly
  messages rather than raw stack traces.
- **Units:** Temperature/wind units are switched live via the `units` command
  and applied to both current weather and forecast requests.
- **Favorites & Exports:** Stored in `data/favorites.json` and `data/exports/`
  respectively — both are safe to delete/reset at any time.

## Possible Future Enhancements

- IP-based automatic location detection (`get_weather_by_ip` is already
  scaffolded in `weather_api.py`)
- Historical weather data lookups
- Weather alerts/warnings integration
- Side-by-side comparison between two cities
