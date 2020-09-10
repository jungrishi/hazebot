import logging
import requests
import typing

from airq import cache
from airq.models.sensors import is_valid_reading


logger = logging.getLogger(__name__)


def get_all_sensor_data() -> typing.List[typing.Dict[str, typing.Any]]:
    try:
        resp = requests.get("https://www.purpleair.com/json")
        resp.raise_for_status()
    except requests.RequestException:
        logger.exception("Error updating purpleair data")
        results = []
    else:
        results = resp.json().get("results", [])
    return results


def _call_purpleair_api(
    sensor_ids: typing.Set[int],
) -> typing.List[typing.Dict[str, typing.Any]]:
    logger.info(
        "Retrieving pm25 data from purpleair for %s sensors", len(sensor_ids),
    )
    try:
        resp = requests.get(
            "https://www.purpleair.com/json?show={}".format(
                "|".join(map(str, sensor_ids))
            )
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.exception(
            "Error retrieving data for sensors %s: %s", sensor_ids, e,
        )
        return []
    else:
        return resp.json().get("results")


def _get_pm25_readings_from_api(sensor_ids: typing.Set[int]) -> typing.Dict[int, float]:
    readings = {}
    dead_sensors = {}

    results = _call_purpleair_api(sensor_ids)
    for r in results:
        if not r.get("ParentID"):
            sensor_id = r["ID"]
            if not is_valid_reading(r):
                dead_sensors[sensor_id] = True
            else:
                sensor_ids.remove(sensor_id)
                pm25 = float(r["PM2_5Value"])
                readings[sensor_id] = pm25

    if dead_sensors:
        cache.DEAD.set_many(dead_sensors)

    if sensor_ids:
        # This should be empty now if we've gotten pm25 info for every sensor.
        logger.warning("No results for ids: %s", sensor_ids)

    if readings:
        cache.READINGS.set_many(readings)

    return readings


def get_pm25_readings(sensor_ids: typing.Set[int]) -> typing.Dict[int, float]:
    dead_sensors = cache.DEAD.get_many(sensor_ids)
    sensor_ids -= set(dead_sensors)

    readings = cache.READINGS.get_many(sensor_ids)
    sensor_ids -= set(readings)

    if sensor_ids:
        readings.update(_get_pm25_readings_from_api(sensor_ids))

    return readings
