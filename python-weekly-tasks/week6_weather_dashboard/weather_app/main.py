"""
main.py
Interactive command-line entry point for the Weather Dashboard Application.
Ties together weather_api, weather_parser, and weather_display into a
usable menu-driven experience with favorites, unit conversion, search,
and CSV export.

Run with:  python -m weather_app.main
"""

import csv
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional

from .config import Config
from .weather_api import WeatherAPI, WeatherAPIError
from .weather_parser import parse_current_weather, parse_forecast, parse_city_search_results
from . import weather_display as display
from dotenv import load_dotenv
load_dotenv()


class WeatherDashboardApp:
    """Main application controller / interactive CLI loop."""

    def __init__(self) -> None:
        Config.ensure_directories()
        self.units = Config.DEFAULT_UNITS  # 'metric' or 'imperial'
        self.api = WeatherAPI(units=self.units)
        self.last_city: Optional[str] = None
        self.favorites: List[Dict] = self._load_favorites()

    # ------------------------------------------------------------------ #
    # Favorites persistence
    # ------------------------------------------------------------------ #
    def _load_favorites(self) -> List[Dict]:
        try:
            with open(Config.FAVORITES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_favorites(self) -> None:
        with open(Config.FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.favorites, f, indent=2)

    def add_favorite(self, city: str) -> str:
        if any(f["city"].lower() == city.lower() for f in self.favorites):
            return f"'{city}' is already in favorites."
        self.favorites.append({"city": city})
        self._save_favorites()
        return f"Added '{city}' to favorites."

    def remove_favorite(self, city: str) -> str:
        before = len(self.favorites)
        self.favorites = [f for f in self.favorites if f["city"].lower() != city.lower()]
        self._save_favorites()
        if len(self.favorites) < before:
            return f"Removed '{city}' from favorites."
        return f"'{city}' was not found in favorites."

    # ------------------------------------------------------------------ #
    # Core actions
    # ------------------------------------------------------------------ #
    def show_weather(self, city: str) -> None:
        try:
            raw_current = self.api.get_current_weather(city)
            current = parse_current_weather(raw_current, self.units)

            raw_forecast = self.api.get_forecast(city)
            forecast = parse_forecast(raw_forecast, self.units)

            print(display.render_header())
            print(display.render_current_weather(current, self.units))
            print(display.render_forecast(forecast, self.units))

            self.last_city = city
        except WeatherAPIError as exc:
            print(display.render_error(str(exc)))

    def refresh_last_city(self) -> None:
        if not self.last_city:
            print(display.render_info("No previous city to refresh. Search for a city first."))
            return
        self.api.clear_cache()
        self.show_weather(self.last_city)

    def search_city(self, query: str) -> None:
        try:
            raw_results = self.api.search_cities(query)
            results = parse_city_search_results(raw_results)
            print(display.render_search_results(results))
        except WeatherAPIError as exc:
            print(display.render_error(str(exc)))

    def toggle_units(self) -> None:
        self.units = "imperial" if self.units == "metric" else "metric"
        self.api.units = self.units
        label = "Fahrenheit" if self.units == "imperial" else "Celsius"
        print(display.render_info(f"Units switched to {label}."))

    def export_city_csv(self, city: str) -> None:
        try:
            raw_current = self.api.get_current_weather(city)
            current = parse_current_weather(raw_current, self.units)
            raw_forecast = self.api.get_forecast(city)
            forecast = parse_forecast(raw_forecast, self.units)
        except WeatherAPIError as exc:
            print(display.render_error(str(exc)))
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_city = city.replace(" ", "_").lower()
        export_path = Config.EXPORT_DIR / f"{safe_city}_{timestamp}.csv"

        with open(export_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Date", "Condition", "Temp", "Temp_Min/Max", "Humidity"])
            writer.writerow(
                [
                    "Current",
                    current["last_updated"],
                    current["description"],
                    f"{current['temperature']}{current['unit_symbol']}",
                    f"{current['temp_min']}/{current['temp_max']}{current['unit_symbol']}",
                    f"{current['humidity']}%",
                ]
            )
            for day in forecast:
                writer.writerow(
                    [
                        "Forecast",
                        day["date"],
                        day["description"],
                        "-",
                        f"{day['temp_min']}/{day['temp_max']}{day['unit_symbol']}",
                        f"{day['humidity_avg']}%",
                    ]
                )

        print(display.render_info(f"Exported weather data to {export_path}"))

    # ------------------------------------------------------------------ #
    # Interactive loop
    # ------------------------------------------------------------------ #
    def run(self) -> None:
        if not Config.validate():
            sys.exit(1)

        print(display.render_header())
        print("Type a city name to check the weather, or 'help' for commands.\n")

        while True:
            try:
                user_input = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye! 👋")
                break

            if not user_input:
                continue

            command, _, arg = user_input.partition(" ")
            command_lower = command.lower()
            arg = arg.strip()

            if command_lower in ("quit", "exit"):
                print("Goodbye! 👋")
                break
            elif command_lower == "help":
                print(display.render_help())
            elif command_lower == "units":
                self.toggle_units()
            elif command_lower == "refresh":
                self.refresh_last_city()
            elif command_lower == "search" and arg:
                self.search_city(arg)
            elif command_lower == "export" and arg:
                self.export_city_csv(arg)
            elif command_lower == "fav":
                sub_command, _, sub_arg = arg.partition(" ")
                sub_arg = sub_arg.strip()
                if sub_command == "add" and sub_arg:
                    print(display.render_info(self.add_favorite(sub_arg)))
                elif sub_command == "remove" and sub_arg:
                    print(display.render_info(self.remove_favorite(sub_arg)))
                elif sub_command == "list":
                    print(display.render_favorites(self.favorites))
                else:
                    print(display.render_error("Usage: fav <add|remove|list> [city]"))
            else:
                # Treat anything else as a city name lookup
                self.show_weather(user_input)


def main() -> None:
    app = WeatherDashboardApp()
    app.run()


if __name__ == "__main__":
    main()
