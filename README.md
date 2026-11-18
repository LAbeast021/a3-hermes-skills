# a3-hermes-skills

Hermes Agent skill tap for CSCI 599 Assignment 3 (Kiarash Hesampour).

## Skills
| Skill | What it does |
|---|---|
| `la-weather-planner` | Keyless weather planner (Open-Meteo): current conditions + 1–3 day forecast for any city, turned into practical advice (what to wear, umbrella, best outdoor window). |

## Install (Hermes)
```bash
hermes skills tap add LAbeast021/a3-hermes-skills
hermes skills install LAbeast021/a3-hermes-skills/skills/la-weather-planner
```
Then ask: *"Use the la-weather-planner skill: what should I wear in Los Angeles tomorrow?"*

No API key needed. Requires Python 3 (stdlib only) and outbound HTTPS to open-meteo.com.
