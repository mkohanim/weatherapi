import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from current_node import CurrentConditions  # noqa: E402
from forecast_node import ForecastDay  # noqa: E402

CUR = {
    'temp_c': 21.5, 'temp_f': 70.7, 'feelslike_c': 20.0, 'feelslike_f': 68.0,
    'dewpoint_c': 10.2, 'dewpoint_f': 50.4, 'humidity': 55, 'cloud': 40,
    'pressure_mb': 1015.0, 'pressure_in': 29.97,
    'wind_mph': 8.1, 'wind_kph': 13.0, 'gust_mph': 12.3, 'gust_kph': 19.8, 'wind_degree': 0,
    'precip_mm': 0.4, 'precip_in': 0.02, 'vis_km': 10.0, 'vis_miles': 6.0,
    'uv': 5.0, 'is_day': 1, 'condition': {'text': 'Sunny', 'code': 1000},
    'air_quality': {'pm2_5': 8.25, 'pm10': 12.5, 'us-epa-index': 2},
}
DAY = {
    'maxtemp_c': 25.0, 'maxtemp_f': 77.0, 'mintemp_c': 12.0, 'mintemp_f': 53.6,
    'maxwind_kph': 30.0, 'maxwind_mph': 18.6, 'totalprecip_mm': 2.5, 'totalprecip_in': 0.1,
    'daily_chance_of_rain': 60, 'daily_chance_of_snow': 0, 'uv': 6.0,
    'condition': {'text': 'Patchy rain nearby', 'code': 1063},
}


def make(cls):
    poly = MagicMock()
    poly.db_getNodeDrivers.return_value = []
    return cls(poly, 'ctl', 'addr', 'name')


def drv(node, name):
    return next(d for d in node.drivers if d['driver'] == name)


def test_st_driver_present_and_old_ids_gone():
    cur = make(CurrentConditions)
    fc = make(ForecastDay)
    assert [d['driver'] for d in cur.drivers].count('ST') == 1
    assert [d['driver'] for d in fc.drivers].count('ST') == 1
    assert 'CLITEMP' not in [d['driver'] for d in cur.drivers]
    assert 'TEMP_HIGH' not in [d['driver'] for d in fc.drivers]


def test_current_us_units():
    n = make(CurrentConditions)
    n.update(CUR, False)
    assert (drv(n, 'ST')['value'], drv(n, 'ST')['uom']) == (70.7, 17)
    assert (drv(n, 'BARPRES')['value'], drv(n, 'BARPRES')['uom']) == (29.97, 23)
    assert (drv(n, 'SPEED')['value'], drv(n, 'SPEED')['uom']) == (8.1, 48)
    assert (drv(n, 'PRECIP')['value'], drv(n, 'PRECIP')['uom']) == (0.02, 105)
    assert (drv(n, 'VISIBILITY')['value'], drv(n, 'VISIBILITY')['uom']) == (6.0, 116)


def test_current_metric_units():
    n = make(CurrentConditions)
    n.update(CUR, True)
    assert (drv(n, 'ST')['value'], drv(n, 'ST')['uom']) == (21.5, 4)
    assert (drv(n, 'BARPRES')['value'], drv(n, 'BARPRES')['uom']) == (1015.0, 117)
    assert (drv(n, 'SPEED')['value'], drv(n, 'SPEED')['uom']) == (13.0, 32)
    assert (drv(n, 'PRECIP')['value'], drv(n, 'PRECIP')['uom']) == (0.4, 82)
    assert (drv(n, 'VISIBILITY')['value'], drv(n, 'VISIBILITY')['uom']) == (10.0, 83)


def test_switching_units_changes_uom():
    n = make(CurrentConditions)
    n.update(CUR, False)
    n.update(CUR, True)
    assert drv(n, 'ST')['uom'] == 4 and drv(n, 'ST')['value'] == 21.5


def test_air_quality_and_flags():
    n = make(CurrentConditions)
    n.update(CUR, False)
    assert drv(n, 'AQI')['value'] == 2
    assert drv(n, 'PM25')['value'] == 8.2 or drv(n, 'PM25')['value'] == 8.3
    assert drv(n, 'DAYNIGHT')['value'] == 1
    assert drv(n, 'COND_CODE')['value'] == 1000


def test_wind_degree_zero_with_wind_is_north_360():
    n = make(CurrentConditions)
    n.update(CUR, False)
    assert drv(n, 'WINDDIR')['value'] == 360


def test_missing_fields_keep_previous_value():
    n = make(CurrentConditions)
    n.update(CUR, False)
    n.update({'condition': {}}, False)
    assert drv(n, 'ST')['value'] == 70.7


def test_forecast_us_and_metric():
    n = make(ForecastDay)
    n.update(DAY, False)
    assert (drv(n, 'ST')['value'], drv(n, 'ST')['uom']) == (77.0, 17)
    assert (drv(n, 'SPEED')['value'], drv(n, 'SPEED')['uom']) == (18.6, 48)
    assert drv(n, 'POP')['value'] == 60
    n.update(DAY, True)
    assert (drv(n, 'TEMP_LOW')['value'], drv(n, 'TEMP_LOW')['uom']) == (12.0, 4)
    assert (drv(n, 'PRECIP')['value'], drv(n, 'PRECIP')['uom']) == (2.5, 82)
