#!/usr/bin/env python3
"""Keyless forecast via Open-Meteo (geocoding + forecast). Stdlib only.

Usage: forecast.py "City name" [days 1-3]
Written for CSCI 599 A3 by Kiarash Hesampour. API docs: https://open-meteo.com/en/docs
"""
import json
import sys
import urllib.parse
import urllib.request

WMO = {0: "clear", 1: "mostly clear", 2: "partly cloudy", 3: "overcast", 45: "fog", 48: "fog",
       51: "light drizzle", 53: "drizzle", 55: "heavy drizzle", 61: "light rain", 63: "rain",
       65: "heavy rain", 71: "light snow", 73: "snow", 75: "heavy snow", 80: "showers",
       81: "showers", 82: "heavy showers", 95: "thunderstorm", 96: "thunderstorm", 99: "thunderstorm"}


def get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read())


def main() -> int:
    city = sys.argv[1] if len(sys.argv) > 1 else "Los Angeles"
    days = max(1, min(3, int(sys.argv[2]) if len(sys.argv) > 2 else 2))
    try:
        g = get("https://geocoding-api.open-meteo.com/v1/search?" +
                urllib.parse.urlencode({"name": city, "count": 1}))
        if not g.get("results"):
            print(json.dumps({"error": f"location not found: {city}"}))
            return 1
        r = g["results"][0]
        f = get("https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
            "latitude": r["latitude"], "longitude": r["longitude"], "timezone": "auto",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
            "current": "temperature_2m,weather_code", "temperature_unit": "fahrenheit",
            "forecast_days": days}))
    except Exception as exc:  # network / API failure -> explicit error, never invented data
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}))
        return 1
    d = f["daily"]
    print(json.dumps({
        "location": f"{r['name']}, {r.get('admin1', '')}".strip(", "),
        "now": f"{f['current']['temperature_2m']}°F, {WMO.get(f['current']['weather_code'], 'n/a')}",
        "daily": [{"date": d["time"][i], "high": d["temperature_2m_max"][i], "low": d["temperature_2m_min"][i],
                   "rainChance": d["precipitation_probability_max"][i],
                   "conditions": WMO.get(d["weather_code"][i], "n/a")} for i in range(len(d["time"]))]},
        indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
