#!/usr/bin/env python3
"""Keyless forecast for the la-weather-planner skill. Stdlib only.

Primary source: Open-Meteo (https://open-meteo.com/en/docs). Fallback: wttr.in JSON
(https://github.com/chubin/wttr.in) when Open-Meteo is unreachable from the network.
Usage: forecast.py "City name" [days 1-3]
Written for CSCI 599 A3 by Kiarash Hesampour.
"""
import json
import sys
import urllib.parse
import urllib.request

WMO = {0: "clear", 1: "mostly clear", 2: "partly cloudy", 3: "overcast", 45: "fog", 48: "fog",
       51: "light drizzle", 53: "drizzle", 55: "heavy drizzle", 61: "light rain", 63: "rain",
       65: "heavy rain", 71: "light snow", 73: "snow", 75: "heavy snow", 80: "showers",
       81: "showers", 82: "heavy showers", 95: "thunderstorm", 96: "thunderstorm", 99: "thunderstorm"}


def get(url: str, timeout: int) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "la-weather-planner/1.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def open_meteo(city: str, days: int) -> dict:
    g = get("https://geocoding-api.open-meteo.com/v1/search?" +
            urllib.parse.urlencode({"name": city, "count": 1}), 8)
    if not g.get("results"):
        return {"error": f"location not found: {city}"}
    r = g["results"][0]
    f = get("https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
        "latitude": r["latitude"], "longitude": r["longitude"], "timezone": "auto",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "current": "temperature_2m,weather_code", "temperature_unit": "fahrenheit",
        "forecast_days": days}), 8)
    d = f["daily"]
    return {"source": "open-meteo", "location": f"{r['name']}, {r.get('admin1', '')}".strip(", "),
            "now": f"{f['current']['temperature_2m']}°F, {WMO.get(f['current']['weather_code'], 'n/a')}",
            "daily": [{"date": d["time"][i], "high": d["temperature_2m_max"][i], "low": d["temperature_2m_min"][i],
                       "rainChance": d["precipitation_probability_max"][i],
                       "conditions": WMO.get(d["weather_code"][i], "n/a")} for i in range(len(d["time"]))]}


def wttr(city: str, days: int) -> dict:
    w = get(f"https://wttr.in/{urllib.parse.quote(city)}?format=j1", 45)
    cur = w["current_condition"][0]
    area = (w.get("nearest_area") or [{}])[0]
    name = (area.get("areaName") or [{"value": city}])[0]["value"]
    daily = []
    for day in w["weather"][:days]:
        hourly = day.get("hourly", [])
        rain = max((int(h.get("chanceofrain", 0)) for h in hourly), default=0)
        desc = hourly[len(hourly) // 2]["weatherDesc"][0]["value"] if hourly else "n/a"
        daily.append({"date": day["date"], "high": float(day["maxtempF"]), "low": float(day["mintempF"]),
                      "rainChance": rain, "conditions": desc.strip().lower()})
    return {"source": "wttr.in", "location": name,
            "now": f"{cur['temp_F']}°F, {cur['weatherDesc'][0]['value'].strip().lower()}", "daily": daily}


def main() -> int:
    city = sys.argv[1] if len(sys.argv) > 1 else "Los Angeles"
    days = max(1, min(3, int(sys.argv[2]) if len(sys.argv) > 2 else 2))
    errors = []
    for fn in (open_meteo, wttr):
        try:
            out = fn(city, days)
            print(json.dumps(out, indent=1, ensure_ascii=False))
            return 0 if "error" not in out else 1
        except Exception as exc:  # unreachable source -> try the next one, never invent data
            errors.append(f"{fn.__name__}: {type(exc).__name__}: {exc}")
    print(json.dumps({"error": "forecast unavailable", "details": errors}))
    return 1


if __name__ == "__main__":
    sys.exit(main())
