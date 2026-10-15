## 2026-10-15T04:23:05.816930+00:00

Initial version. Controller + Current Conditions node + N Forecast Day nodes (N = forecast_days, 1-14) for WeatherAPI.com. One forecast.json?aqi=yes call per 15 min poll. US/metric chosen via the units custom param: editors carry both unit ranges (F/C, mph/km/h, inHg/mb, in/mm, mi/km) and setDriver is given the matching uom. Air quality (US EPA index, PM2.5, PM10) included; sunrise/sunset deliberately excluded. API errors surfaced as Notices; API key never logged.

## 2026-10-15T06:48:57.765957+00:00

Renamed the main property on each non-controller node to the standard ST id so the profile passes validation: CLITEMP -> ST (Current Conditions, 'Temperature') and TEMP_HIGH -> ST (Forecast Day, 'High Temperature'). Updated drivers, update() calls and tests accordingly. Behavior otherwise unchanged. Note: programs/scenes referencing the old CLITEMP/TEMP_HIGH ids must be repointed to ST.

