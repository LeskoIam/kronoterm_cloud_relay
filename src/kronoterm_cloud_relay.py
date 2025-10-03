__version__ = "0.0.24"

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every
from kronoterm_cloud_api.client import KronotermCloudApi, KronotermCloudApiException
from kronoterm_cloud_api.kronoterm_enums import (
    HeatingLoop,
    HeatingLoopMode,
    HeatingLoopStatus,
    HeatPumpOperatingMode,
    WorkingFunction,
)
from prometheus_client import Gauge, Info, make_asgi_app

from src.config import KRONOTERM_CLOUD_PASSWORD, KRONOTERM_CLOUD_USER, PROMETHEUS_UPDATE_INTERVAL, configure_logging

configure_logging()
log = logging.getLogger("relay")


hp_api = KronotermCloudApi(username=KRONOTERM_CLOUD_USER, password=KRONOTERM_CLOUD_PASSWORD)
hp_api.login()
hp_api.update_heat_pump_basic_information()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """https://fastapi.tiangolo.com/advanced/events/"""
    # repeat_every decorated function must be called at startup to start the repeat mechanism
    await hp_data_to_prometheus()
    log.info("Initial data gathering done.")
    yield
    log.info("Exiting...")


app = FastAPI(lifespan=lifespan)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Prometheus metrics
hp_info = Info("basic", "Heat pump information", namespace="heat_pump")
hp_temperatures_gauge = Gauge(
    "temperature_c", "Heat pump temperatures [°C]", namespace="heat_pump", labelnames=["heating_loop", "name"]
)
hp_power_consumption_gauge = Gauge(
    "power_consumption_kwh", "Heat pump power consumption [kWh]", namespace="heat_pump", labelnames=["function"]
)
hp_pressure_gauge = Gauge("pressure_bar", "Heat pump system pressure [bar]", namespace="heat_pump")
hp_function_gauge = Gauge(
    "function", "Heat pump function", namespace="heat_pump", labelnames=["heating_loop", "function"]
)


@repeat_every(seconds=PROMETHEUS_UPDATE_INTERVAL)
async def hp_data_to_prometheus():
    """Update prometheus shared data.

    Update interval controlled by PROMETHEUS_UPDATE_INTERVAL environment variable.
    """
    __info_summary()


def __info_summary() -> dict:
    """Summary.

    :return: summary
    """
    system_review_data = hp_api.get_system_review_data()
    loop_1_data = hp_api.get_heating_loop_data(HeatingLoop.HEATING_LOOP_1)
    loop_2_data = hp_api.get_heating_loop_data(HeatingLoop.HEATING_LOOP_2)
    loop_5_data = hp_api.get_heating_loop_data(HeatingLoop.TAP_WATER)
    alarms_data = hp_api.get_alarms_data()["AlarmsData"]
    power_consumption_data = hp_api.get_theoretical_power_consumption()

    room_temperature = float(system_review_data["TemperaturesAndConfig"]["heating_circle_2_temp"])
    outlet_temperature = float(system_review_data["CurrentFunctionData"][0]["dv_temp"])
    try:
        heating_system_pressure = float(system_review_data["CurrentFunctionData"][0]["heating_system_pressure"])
    except KeyError:
        # This should go away in kronoterm_cloud_relay v0.0.23 using kronoterm_cloud_api v0.1.17
        log.warning("Missing info: 'heating_system_pressure'")
        heating_system_pressure = -1
    outside_temperature = float(system_review_data["TemperaturesAndConfig"]["outside_temp"])
    sanitary_water_temperature = float(system_review_data["TemperaturesAndConfig"]["tap_water_temp"])
    working_function = system_review_data["TemperaturesAndConfig"]["working_function"]
    heat_pump_operating_mode = HeatPumpOperatingMode(system_review_data["TemperaturesAndConfig"]["main_mode"])

    heating_loop_1_current_temp = float(system_review_data["SystemData"][1]["circle_temp"])
    heating_loop_1_target_temp = float(loop_1_data["HeatingCircleData"]["circle_temp"])
    cal_target = float(loop_1_data["HeatingCircleData"]["circle_calc_temp"])
    heating_loop_1_calc_target_temp = 0.0 if cal_target > 499 else cal_target
    heating_loop_1_working_status = loop_1_data["HeatingCircleData"]["circle_status"]
    heating_loop_1_working_mode = loop_1_data["HeatingCircleData"]["circle_mode"]

    heating_loop_2_target_temp = float(loop_2_data["HeatingCircleData"]["circle_temp"])
    cal_target = float(loop_2_data["HeatingCircleData"]["circle_calc_temp"])
    heating_loop_2_calc_target_temp = 0.0 if cal_target > 499 else cal_target
    heating_loop_2_working_status = loop_2_data["HeatingCircleData"]["circle_status"]
    heating_loop_2_working_mode = loop_2_data["HeatingCircleData"]["circle_mode"]

    heating_loop_5_target_temp = float(loop_5_data["HeatingCircleData"]["circle_temp"])
    cal_target = float(loop_5_data["HeatingCircleData"]["circle_calc_temp"])
    heating_loop_5_calc_target_temp = 0.0 if cal_target > 499 else cal_target
    heating_loop_5_working_status = loop_5_data["HeatingCircleData"]["circle_status"]
    heating_loop_5_working_mode = loop_5_data["HeatingCircleData"]["circle_mode"]

    # Prometheus
    # Temperature
    hp_temperatures_gauge.labels("system", "room_temperature").set(room_temperature)
    hp_temperatures_gauge.labels("system", "outlet_temperature").set(outlet_temperature)
    hp_temperatures_gauge.labels("system", "outside_temperature").set(outside_temperature)
    hp_temperatures_gauge.labels("system", "sanitary_water_temperature").set(sanitary_water_temperature)

    hp_temperatures_gauge.labels("loop_1", "current_temp").set(heating_loop_1_current_temp)
    hp_temperatures_gauge.labels("loop_1", "target_temp").set(heating_loop_1_target_temp)
    hp_temperatures_gauge.labels("loop_1", "calc_target_temp").set(heating_loop_1_calc_target_temp)

    hp_temperatures_gauge.labels("loop_2", "target_temp").set(heating_loop_2_target_temp)
    hp_temperatures_gauge.labels("loop_2", "calc_target_temp").set(heating_loop_2_calc_target_temp)

    hp_temperatures_gauge.labels("loop_5", "target_temp").set(heating_loop_5_target_temp)
    hp_temperatures_gauge.labels("loop_5", "calc_target_temp").set(heating_loop_5_calc_target_temp)
    # Power consumption
    hp_power_consumption_gauge.labels("heating").set(power_consumption_data.heating)
    hp_power_consumption_gauge.labels("cooling").set(power_consumption_data.cooling)
    hp_power_consumption_gauge.labels("tap_water").set(power_consumption_data.tap_water)
    hp_power_consumption_gauge.labels("pumps").set(power_consumption_data.pumps)
    hp_power_consumption_gauge.labels("total").set(power_consumption_data.all)
    # Pressure
    hp_pressure_gauge.set(heating_system_pressure)
    # Function
    hp_function_gauge.labels("system", "operating_mode").set(heat_pump_operating_mode.value)
    hp_function_gauge.labels("system", "working_function").set(working_function)

    hp_function_gauge.labels("loop_1", "working_status").set(heating_loop_1_working_status)
    hp_function_gauge.labels("loop_1", "working_mode").set(heating_loop_1_working_mode)

    hp_function_gauge.labels("loop_2", "working_status").set(heating_loop_2_working_status)
    hp_function_gauge.labels("loop_2", "working_mode").set(heating_loop_2_working_mode)

    hp_function_gauge.labels("loop_5", "working_status").set(heating_loop_5_working_status)
    hp_function_gauge.labels("loop_5", "working_mode").set(heating_loop_5_working_mode)
    # Info
    hp_info.info(
        {"hp_id": str(hp_api.hp_id), "location_name": str(hp_api.location_name), "user_level": str(hp_api.user_level)}
    )

    output = {
        "hp_id": hp_api.hp_id,
        "location_name": hp_api.location_name,
        "user_level": hp_api.user_level,
        "heating_loop_names": hp_api.loop_names,
        "alarms": alarms_data,
        "heat_pump_operating_mode": heat_pump_operating_mode.name,
        "system_info": {
            "room_temperature": room_temperature,
            "outlet_temperature": outlet_temperature,
            "outside_temperature": outside_temperature,
            "sanitary_water_temperature": sanitary_water_temperature,
            "heating_system_pressure": heating_system_pressure,
            "working_function": WorkingFunction(working_function).name,
            "power_consumption_heating": power_consumption_data.heating,
            "power_consumption_cooling": power_consumption_data.cooling,
            "power_consumption_tap_water": power_consumption_data.tap_water,
            "power_consumption_pumps": power_consumption_data.pumps,
            "power_consumption_total": power_consumption_data.all,
        },
        "heating_loop_1": {
            "current_temp": heating_loop_1_current_temp,
            "target_temp": heating_loop_1_target_temp,
            "calc_target_temp": heating_loop_1_calc_target_temp,
            "working_status": HeatingLoopStatus(heating_loop_1_working_status).name,
            "working_mode": HeatingLoopMode(heating_loop_1_working_mode).name,
        },
        "heating_loop_2": {
            "target_temp": heating_loop_2_target_temp,
            "calc_target_temp": heating_loop_2_calc_target_temp,
            "working_status": HeatingLoopStatus(heating_loop_2_working_status).name,
            "working_mode": HeatingLoopMode(heating_loop_2_working_mode).name,
        },
        "heating_loop_5": {
            "target_temp": heating_loop_5_target_temp,
            "calc_target_temp": heating_loop_5_calc_target_temp,
            "working_status": HeatingLoopStatus(heating_loop_5_working_status).name,
            "working_mode": HeatingLoopMode(heating_loop_5_working_mode).name,
        },
    }
    return output


@app.get("/")
def about():
    """Return API name and version"""
    return {"detail": "kronoterm-cloud-relay", "version": __version__}


@app.post("/api/v1/echo/{msg}")
def echo(msg: str):
    """Echo into the void"""
    return {"echo": msg}


@app.get("/api/v1/info-summary")
def info_summary() -> dict:
    """
    Retrieves a summary of heat pump information.
    It's mostly for use with HomeAssistant or similar systems to limit calls to external API.

    :return: A dictionary containing the summary data.
    """
    return {"data": __info_summary()}


@app.get("/api/v1/initial-data")
def initial_data():
    """Get initial data"""
    return {"data": hp_api.get_initial_data()}


@app.get("/api/v1/basic-data")
def basic_data():
    """Get basic data"""
    return {"data": hp_api.get_basic_data()}


@app.get("/api/v1/system-review")
def system_review():
    """Get system review data"""
    return {"data": hp_api.get_system_review_data()}


@app.get("/api/v1/heating-loop/{loop_id}")
def heating_loop(loop_id: int):
    """Get heating loop data

    :param loop_id: id of the loop for which data will be returned
    """
    values = set(item.value for item in HeatingLoop)  # WA
    if loop_id not in values:
        raise HTTPException(status_code=404, detail=f"heating loop '{loop_id}' not supported")
    hl = HeatingLoop(loop_id)
    log.info("heating loop data for %s", hl)
    return {"data": hp_api.get_heating_loop_data(hl)}


@app.get("/api/v1/alarms")
def alarms():
    """Get alarms data"""
    return {"data": hp_api.get_alarms_data()}


@app.post("/api/v1/target-temperature/{loop_id}/{target_temperature}")
def set_target_temperature(loop_id: int, target_temperature: float | int):
    """Set temperature of the heating loop

    :param loop_id: heating loop id
    :param target_temperature: temperature to set the loop to
    """
    values = set(item.value for item in HeatingLoop)  # WA
    if loop_id not in values:
        raise HTTPException(status_code=404, detail=f"heating loop '{loop_id}' not supported")
    hl = HeatingLoop(loop_id)
    max_temp = 28
    if hl == HeatingLoop.TAP_WATER:
        max_temp = 60
    if not (16 <= target_temperature <= max_temp):
        raise HTTPException(
            status_code=400,
            detail=f"temperature colder than 16 and hotter than {max_temp} Celsius not supported for {hl}",
        )
    hl = HeatingLoop(loop_id)
    hp_api.set_heating_loop_target_temperature(hl, target_temperature)
    return {
        "detail": f"Set temperature of '{hl.name}' to {target_temperature} degrees Celsius",
        "telemetry_check": hp_api.get_heating_loop_target_temperature(hl) == target_temperature,
    }


@app.post("/api/v1/loop-mode/{loop_id}/{mode}")
def set_heating_loop_mode(loop_id: int, mode: str):
    """Set mode of the heating loop

    :param loop_id: heating loop id
    :param mode: mode to set the loop to
    """
    values = set(item.value for item in HeatingLoop)  # WA
    if loop_id not in values:
        raise HTTPException(status_code=404, detail=f"heating loop '{loop_id}' not supported")
    mode = mode.upper()
    if mode not in ("AUTO", "ON", "OFF"):
        raise HTTPException(status_code=400, detail=f"loop mode {mode} not supported")
    hl = HeatingLoop(loop_id)
    hl_mode = HeatingLoopMode[mode]
    hp_api.set_heating_loop_mode(hl, hl_mode)
    return {
        "detail": f"Set mode of '{hl.name}' to {hl_mode}",
        "telemetry_check": hp_api.get_heating_loop_mode(hl) == hl_mode,
    }


@app.post("/api/v1/heatpump-mode/{mode}")
def set_heat_pump_operating_mode(mode: str):
    """Set heat pump operating mode

    :param mode: mode to set the loop to
    """
    if mode not in ("COMFORT", "AUTO", "ECO"):
        raise HTTPException(status_code=400, detail=f"heat pump operating mode {mode} not supported")
    hp_mode = HeatPumpOperatingMode[mode]
    hp_api.set_heat_pump_operating_mode(hp_mode)
    return {
        "detail": f"Set heat pump operating mode to {hp_mode}",
        "telemetry_check": hp_api.get_heat_pump_operating_mode() == hp_mode,
    }


@app.post("/api/v1/refresh-login")
def refresh_login():
    """
    Refresh the login session with the Kronoterm Cloud API.

    :raises HTTPException: If the login attempt fails, an HTTPException is raised with a status code of 503
            and the exception detail.
    :return: A JSON response indicating that the login refresh was successful.
    """
    try:
        hp_api.login()
    except KronotermCloudApiException as exc:
        return HTTPException(status_code=503, detail=str(exc))
    return {"detail": "Login refresh successful"}


@app.post("/api/v1/refresh-basic-info")
def refresh_basic_information():
    """
    Refresh the basic information of the heat pump from the Kronoterm Cloud API.

    :return: A JSON response indicating that the basic information refresh was successful.
    """
    hp_api.update_heat_pump_basic_information()
    return {"detail": "Basic information refresh successful"}
