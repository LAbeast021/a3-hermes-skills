---
name: la-weather-planner
description: Keyless weather planner. Fetches current conditions and a 1-3 day forecast for any city from Open-Meteo and turns it into practical advice (clothing, umbrella, best time to be outside). Use when the user asks about weather, what to wear, or planning outdoor time.
version: 1.0.0
author: Kiarash Hesampour (CSCI 599 A3)
license: MIT
metadata:
  hermes:
    tags: [weather, planning, briefing]
---

# LA Weather Planner

Use this skill when the user asks about the weather, what to wear, whether to bring an
umbrella, or when to schedule something outdoors.

## How to use

1. Work out the city (default: **Los Angeles**) and how many days (1-3, default 2).
2. Run the bundled script with the terminal tool:

   ```bash
   python3 "$(find "${HERMES_HOME:-$HOME/.hermes}/skills" -path '*la-weather-planner/scripts/forecast.py' | head -1)" "Los Angeles" 2
   ```

   The script prints JSON: `location`, `now`, and `daily[]` with `high`, `low` (°F),
   `rainChance` (%) and `conditions`.
3. Answer in 3-5 short bullets:
   - current conditions, then each day's high/low and conditions
   - **Wear:** <60°F jacket · 60-75°F light layer · >75°F light clothes
   - **Umbrella:** yes if `rainChance` ≥ 40%
   - **Best outdoor window:** the warmer, drier part of the day
4. If the script prints an `error`, say the forecast is unavailable and do not invent numbers.

## Rules
- Never guess weather values; only report what the script returned.
- The script is read-only: it makes two HTTPS GET requests and writes nothing.
