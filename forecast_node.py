"""Forecast Day node for WeatherAPI.com."""

import udi_interface

LOGGER = udi_interface.LOGGER


def _num(src, key):
    """Return src[key] as a float, or None if missing/not numeric."""
    try:
        v = src.get(key)
        return None if v is None else float(v)
    except (TypeError, ValueError, AttributeError):
        return None


class ForecastDay(udi_interface.Node):
    id = '131313_forecast'
    # Default uoms are the US ones; update() passes the right uom on every set.
    # ST is the node's status value: the day's high temperature.
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 17, 'name': 'High Temperature'},
        {'driver': 'TEMP_LOW', 'value': 0, 'uom': 17, 'name': 'Low Temperature'},
        {'driver': 'POP', 'value': 0, 'uom': 51, 'name': 'Chance of Rain'},
        {'driver': 'POP_SNOW', 'value': 0, 'uom': 51, 'name': 'Chance of Snow'},
        {'driver': 'PRECIP', 'value': 0, 'uom': 105, 'name': 'Total Precipitation'},
        {'driver': 'SPEED', 'value': 0, 'uom': 48, 'name': 'Max Wind Speed'},
        {'driver': 'UV', 'value': 0, 'uom': 71, 'name': 'UV Index'},
        {'driver': 'COND_CODE', 'value': 0, 'uom': 56, 'name': 'Condition Code'},
    ]

    def _put(self, driver, value, uom, prec=1, text=None):
        if value is None:
            return  # field missing from this response: keep the last value
        value = round(value, prec) if prec else int(round(value))
        if text is None:
            self.setDriver(driver, value, uom=uom)
        else:
            self.setDriver(driver, value, uom=uom, text=text)

    def update(self, day, metric):
        """Apply the 'day' object of one forecastday entry."""
        day = day or {}
        m = bool(metric)
        sfx = 'c' if m else 'f'
        t_uom = 4 if m else 17

        self._put('ST', _num(day, 'maxtemp_' + sfx), t_uom)
        self._put('TEMP_LOW', _num(day, 'mintemp_' + sfx), t_uom)
        self._put('POP', _num(day, 'daily_chance_of_rain'), 51, 0)
        self._put('POP_SNOW', _num(day, 'daily_chance_of_snow'), 51, 0)
        if m:
            self._put('PRECIP', _num(day, 'totalprecip_mm'), 82, 1)
            self._put('SPEED', _num(day, 'maxwind_kph'), 32, 1)
        else:
            self._put('PRECIP', _num(day, 'totalprecip_in'), 105, 2)
            self._put('SPEED', _num(day, 'maxwind_mph'), 48, 1)
        self._put('UV', _num(day, 'uv'), 71)
        cond = day.get('condition') or {}
        self._put('COND_CODE', _num(cond, 'code'), 56, 0, text=cond.get('text'))
