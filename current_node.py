"""Current Conditions node for WeatherAPI.com."""

import udi_interface

LOGGER = udi_interface.LOGGER


def _num(src, key):
    """Return src[key] as a float, or None if missing/not numeric."""
    try:
        v = src.get(key)
        return None if v is None else float(v)
    except (TypeError, ValueError, AttributeError):
        return None


class CurrentConditions(udi_interface.Node):
    id = '131313_current'
    # Default uoms are the US ones; update() passes the right uom on every set.
    # ST is the node's status value: the current temperature.
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 17, 'name': 'Temperature'},
        {'driver': 'FEELS_LIKE', 'value': 0, 'uom': 17, 'name': 'Feels Like'},
        {'driver': 'DEWPT', 'value': 0, 'uom': 17, 'name': 'Dew Point'},
        {'driver': 'CLIHUM', 'value': 0, 'uom': 51, 'name': 'Humidity'},
        {'driver': 'BARPRES', 'value': 0, 'uom': 23, 'name': 'Pressure'},
        {'driver': 'SPEED', 'value': 0, 'uom': 48, 'name': 'Wind Speed'},
        {'driver': 'GUST', 'value': 0, 'uom': 48, 'name': 'Wind Gust'},
        {'driver': 'WINDDIR', 'value': 0, 'uom': 76, 'name': 'Wind Direction'},
        {'driver': 'CLOUD_COVER', 'value': 0, 'uom': 51, 'name': 'Cloud Cover'},
        {'driver': 'UV', 'value': 0, 'uom': 71, 'name': 'UV Index'},
        {'driver': 'PRECIP', 'value': 0, 'uom': 105, 'name': 'Precipitation'},
        {'driver': 'VISIBILITY', 'value': 0, 'uom': 116, 'name': 'Visibility'},
        {'driver': 'COND_CODE', 'value': 0, 'uom': 56, 'name': 'Condition Code'},
        {'driver': 'DAYNIGHT', 'value': 0, 'uom': 25, 'name': 'Day/Night'},
        {'driver': 'AQI', 'value': 0, 'uom': 25, 'name': 'Air Quality (US EPA)'},
        {'driver': 'PM25', 'value': 0, 'uom': 122, 'name': 'PM2.5'},
        {'driver': 'PM10', 'value': 0, 'uom': 122, 'name': 'PM10'},
    ]

    def _put(self, driver, value, uom, prec=1, text=None):
        if value is None:
            return  # field missing from this response: keep the last value
        value = round(value, prec) if prec else int(round(value))
        if text is None:
            self.setDriver(driver, value, uom=uom)
        else:
            self.setDriver(driver, value, uom=uom, text=text)

    def update(self, cur, metric):
        """Apply the 'current' object of a WeatherAPI.com response."""
        cur = cur or {}
        m = bool(metric)
        sfx = 'c' if m else 'f'
        t_uom = 4 if m else 17
        s_uom = 32 if m else 48

        self._put('ST', _num(cur, 'temp_' + sfx), t_uom)
        self._put('FEELS_LIKE', _num(cur, 'feelslike_' + sfx), t_uom)
        self._put('DEWPT', _num(cur, 'dewpoint_' + sfx), t_uom)
        self._put('CLIHUM', _num(cur, 'humidity'), 51, 0)
        if m:
            self._put('BARPRES', _num(cur, 'pressure_mb'), 117, 1)
        else:
            self._put('BARPRES', _num(cur, 'pressure_in'), 23, 2)

        speed = _num(cur, 'wind_kph' if m else 'wind_mph')
        self._put('SPEED', speed, s_uom)
        self._put('GUST', _num(cur, 'gust_kph' if m else 'gust_mph'), s_uom)
        deg = _num(cur, 'wind_degree')
        if deg is not None:
            # uom 76 reserves 0 for 'no wind'; north is 360.
            if deg == 0 and speed:
                deg = 360
            self._put('WINDDIR', deg, 76, 0)

        self._put('CLOUD_COVER', _num(cur, 'cloud'), 51, 0)
        self._put('UV', _num(cur, 'uv'), 71)
        if m:
            self._put('PRECIP', _num(cur, 'precip_mm'), 82, 1)
            self._put('VISIBILITY', _num(cur, 'vis_km'), 83, 1)
        else:
            self._put('PRECIP', _num(cur, 'precip_in'), 105, 2)
            self._put('VISIBILITY', _num(cur, 'vis_miles'), 116, 1)

        cond = cur.get('condition') or {}
        self._put('COND_CODE', _num(cond, 'code'), 56, 0, text=cond.get('text'))
        self._put('DAYNIGHT', _num(cur, 'is_day'), 25, 0)

        aq = cur.get('air_quality') or {}
        self._put('AQI', _num(aq, 'us-epa-index'), 25, 0)
        self._put('PM25', _num(aq, 'pm2_5'), 122, 1)
        self._put('PM10', _num(aq, 'pm10'), 122, 1)
