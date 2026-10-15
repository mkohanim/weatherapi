# WeatherAPI

An eisy/IoX plugin that brings weather from [WeatherAPI.com](https://www.weatherapi.com/) into eisy for a single location.

## What you get

- **Current Conditions** node: temperature (the node's status value), feels-like, dew point, humidity, pressure, wind speed / gust / direction, cloud cover, UV index, precipitation, visibility, condition code, day/night, and air quality (US EPA index, PM2.5, PM10).
- **Forecast nodes** (Today, Tomorrow, Day 3, ...): high temperature (the node's status value), low temperature, chance of rain, chance of snow, total precipitation, max wind speed, UV index and condition code.
- **Refresh Now** command on the controller node.

## Setup

1. Create a free key at weatherapi.com.
2. Install the plugin and open its configuration page.
3. Fill in the custom parameters:
   - `api_key` - your WeatherAPI.com key
   - `location` - city, `lat,lon`, or postcode
   - `units` - `us` or `metric`
   - `forecast_days` - 1 to 14 (limited by your WeatherAPI.com plan)

## How it works

One call to `forecast.json` (with `aqi=yes`) per update returns current conditions, the forecast and air quality together, so each update costs a single API call. Updates run every 15 minutes (long poll).

Each unit-dependent value carries both unit systems in its editor, and the plugin reports the unit chosen by `units`. Sunrise/sunset is not included in this version.

## Upgrading to 1.1.0

The Current Conditions temperature moved from property id `CLITEMP` to `ST`, and the Forecast Day high temperature from `TEMP_HIGH` to `ST`. Programs or scenes that referenced the old ids need to be pointed at `ST`.

## Errors

API problems (invalid or missing key, location not found, quota exceeded, key disabled, plan restriction, network failure) show up as notices on the configuration page. The API key is never written to the log.

## License Notice

This plugin's development referenced the following source(s), whose license is not on the standard permissive allowlist. Review their license terms before relying on or redistributing this plugin:

- [GitHub - wadjaafar/android-geofencing: Creating monitored regions using Android Geofencing API · GitHub](https://github.com/wadjaafar/android-geofencing) -- license: unknown

See LICENSE.md for full third-party attribution.
