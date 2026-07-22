"""
config.py
Loads configuration and environment variables (API keys, base URLs, cache settings)
for the Weather Dashboard Application.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed - fall back to plain os.environ
    pass


class Config:
    """Central configuration for the weather app."""

    # --- API Settings ---
    API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    BASE_URL: str = os.getenv(
        "OPENWEATHER_BASE_URL", "https://api.openweathermap.org/data/2.5"
    )
    GEOCODE_URL: str = os.getenv(
        "OPENWEATHER_GEOCODE_URL", "https://api.openweathermap.org/geo/1.0"
    )

    # --- Request Settings ---
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))

    # --- Cache Settings ---
    CACHE_DURATION: int = int(os.getenv("CACHE_DURATION", "600"))  # seconds
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    CACHE_DIR: Path = PROJECT_ROOT / "data" / "cache"
    FAVORITES_FILE: Path = PROJECT_ROOT / "data" / "favorites.json"
    EXPORT_DIR: Path = PROJECT_ROOT / "data" / "exports"

    # --- Display Settings ---
    DEFAULT_UNITS: str = os.getenv("DEFAULT_UNITS", "metric")  # metric | imperial

    @classmethod
    def validate(cls) -> bool:
        """Check that required configuration is present."""
        if not cls.API_KEY:
            print(
                "⚠️  No API key found. Copy .env.example to .env and add your "
                "OPENWEATHER_API_KEY."
            )
            return False
        return True

    @classmethod
    def ensure_directories(cls) -> None:
        """Create required data directories if they don't exist."""
        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cls.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        if not cls.FAVORITES_FILE.exists():
            cls.FAVORITES_FILE.write_text("[]", encoding="utf-8")
