from typing import Any
from datetime import datetime
import os
import json
import requests

from skyfield.api import load, Loader
from skyfield.framelib import ecliptic_frame
from skyfield import eclipselib

from mcp.server.fastmcp import FastMCP


# Initialize FastMCP server
mcp = FastMCP("star-gazing", dependencies=["requests", "skyfield"])

# Use a custom writable directory for Skyfield ephemeris files
load = Loader('/tmp/skyfield')
eph = load('de421.bsp')


def compute_event_time(iso_datetime: str):
    """
    Convert ISO 8601 datetime string to a Skyfield time object.

    Parameters:
        iso_datetime (str): Date and time in ISO 8601 format, e.g., '2026-01-01T14:30'
    """
    dt = datetime.fromisoformat(iso_datetime)
    ts = load.timescale()
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    return t


@mcp.tool()
def get_lunar_eclipse(starting_time_iso_datetime: str, ending_time_iso_datetime: str) -> str:
    """Return the lunar eclipse details between ``start_time`` and ``end_time``."""
    t0 = compute_event_time(starting_time_iso_datetime)
    t1 = compute_event_time(ending_time_iso_datetime)
    t, y, details = eclipselib.lunar_eclipses(t0, t1, eph)

    dict_details = {}
    for ti, yi in zip(t, y):
        dict_details[ti.utc_strftime('%Y-%m-%d %H:%M')] = [
            f'y={yi}',
            eclipselib.LUNAR_ECLIPSES[yi],
            {}
        ]

    for detail in details:
        for ti, di in zip(t, details[detail]):
            dict_details[ti.utc_strftime('%Y-%m-%d %H:%M')][2][detail] = di

    return json.dumps(dict_details, default=str, indent=2)


@mcp.tool()
def get_moon_phase(iso_datetime: str) -> dict[str, Any]:
    """Get current moon phase based on time of the place on Earth."""
    t = compute_event_time(iso_datetime)
    sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

    e = earth.at(t)
    s = e.observe(sun).apparent()
    m = e.observe(moon).apparent()

    _, slon, _ = s.frame_latlon(ecliptic_frame)
    _, mlon, _ = m.frame_latlon(ecliptic_frame)
    phase = (mlon.degrees - slon.degrees) % 360.0
    percent = 100.0 * m.fraction_illuminated(sun)

    return {"Phase": phase, "Percent": percent}


@mcp.tool()
def get_weather(city: str) -> dict[str, Any]:
    """Get current weather for a location using OpenWeather API."""
    api_key = os.getenv("OPENWEATHER_API_KEY")

    # Get the latitude and longitude of the city
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_data = requests.get(geo_url).json()
    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    # Get the current weather
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )
    weather_data = requests.get(weather_url).json()
    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["main"]

    return {
        "location": city,
        "temperature": temperature,
        "description": description,
    }


if __name__ == "__main__":
    mcp.run()
