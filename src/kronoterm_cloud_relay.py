__version__ = "0.0.6"

import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api, Resource, reqparse
from kronoterm_cloud_api.client import KronotermCloudApi
from kronoterm_cloud_api.kronoterm_enums import HeatingLoop, HeatingLoopMode, HeatingLoopStatus, WorkingFunction

from util.logz import create_logger

log = create_logger(__name__)

load_dotenv()

hp_api = KronotermCloudApi(username=os.getenv("KRONOTERM_CLOUD_USER"), password=os.getenv("KRONOTERM_CLOUD_PASSWORD"))
hp_api.login()
hp_api.update_heat_pump_basic_information()

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("temperature", type=float)
parser.add_argument("mode", type=str)
# HeatingLoop.HEATING_LOOP_1 = 1
# HeatingLoop.HEATING_LOOP_2 = 2
# HeatingLoop.TAP_WATER = 5
parser.add_argument("heating_loop", type=int)


def info_summary() -> dict:
    """Summary.

    :return: summary
    """
    system_review_data = hp_api.get_system_review_data()
    loop_1_data = hp_api.get_heating_loop_data(HeatingLoop.HEATING_LOOP_1)
    loop_2_data = hp_api.get_heating_loop_data(HeatingLoop.HEATING_LOOP_2)
    alarms_data = hp_api.get_alarms_data()["AlarmsData"]
    power_consumption_data = hp_api.get_theoretical_power_consumption()

    room_temperature = float(system_review_data["TemperaturesAndConfig"]["heating_circle_2_temp"])
    outlet_temperature = float(system_review_data["CurrentFunctionData"][0]["dv_temp"])
    heating_system_pressure = float(system_review_data["CurrentFunctionData"][0]["heating_system_pressure"])
    outside_temperature = float(system_review_data["TemperaturesAndConfig"]["outside_temp"])
    sanitary_water_temperature = float(system_review_data["TemperaturesAndConfig"]["tap_water_temp"])
    working_function = system_review_data["TemperaturesAndConfig"]["working_function"]

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

    output = {
        "hp_id": hp_api.hp_id,
        "location_name": hp_api.location_name,
        "user_level": hp_api.user_level,
        "heating_loop_names": hp_api.loop_names,
        "alarms": alarms_data,
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
    }
    return output


class HPInfo(Resource):
    def get(self, about, heating_loop=None):
        """Get heat pump data based on `about` argument.

        hp_info
        /hp_info/<string:about>
        """
        values = set(item.value for item in HeatingLoop)  # WA
        if heating_loop is not None and heating_loop not in values:
            return {"message": f"Heating loop '{heating_loop}' not supported"}, 404
        match about:
            case "info_summary":
                return {"data": info_summary()}
            case "initial_data":
                return {"data": hp_api.get_initial_data()}
            case "basic_data":
                return {"data": hp_api.get_basic_data()}
            case "system_review":
                return {"data": hp_api.get_system_review_data()}
            case "heating_loop":
                heating_loop = HeatingLoop(heating_loop)
                log.info("heating loop data for %s", heating_loop)
                return {"data": hp_api.get_heating_loop_data(heating_loop)}
            case "alarms":
                return {"data": hp_api.get_alarms_data()}
            case _:
                return f"hp_info/{about} not supported", 404


class HPController(Resource):
    def post(self, operation):
        """Set heat pump temperature and operation mode.

        hp_control
        /hp_control/<string:operation>/
        payload = {"heating_loop": kronoterm_enums.HeatingLoop.value}
        """
        args = parser.parse_args()
        heating_loop = args.get("heating_loop")
        values = set(item.value for item in HeatingLoop)  # WA
        if heating_loop not in values:
            return {"message": f"Heating loop '{heating_loop}' not supported"}, 404
        heating_loop = HeatingLoop(heating_loop)
        match operation:
            case "set_target_temperature":
                temp = args.get("temperature")
                if temp is not None:
                    hp_api.set_heating_loop_target_temperature(heating_loop, temp)
                    return {
                        "message": f"Set temperature of '{heating_loop.name}' to {temp} degrees Celsius",
                        "telemetry_check": hp_api.get_heating_loop_target_temperature(heating_loop) == temp,
                    }
                else:
                    return {"message": "set-temperature arg/s missing"}, 404

            case "set_heating_loop_mode":
                mode = args.get("mode").upper()
                if mode is not None:
                    mode = mode.upper()
                    if mode == "ON":
                        hp_api.set_heating_loop_mode(heating_loop, HeatingLoopMode.ON)
                    elif mode == "OFF":
                        hp_api.set_heating_loop_mode(heating_loop, HeatingLoopMode.OFF)
                    elif mode == "AUTO":
                        hp_api.set_heating_loop_mode(heating_loop, HeatingLoopMode.AUTO)
                    else:
                        return {"message": f"Invalid mode {mode} for 'set_heating_loop_mode'"}, 404
                    return {"message": f"Set heating loop {heating_loop.name} mode to {mode}"}
                else:
                    return {"message": "'mode' not set"}, 404
            case _:
                return {"message": f"'{operation}': Invalid operation"}, 404


class RelayController(Resource):
    def get(self, operation, optional=None):
        """Healthcheck endpoint"""
        match operation:
            case "echo":
                return {"message": f"relay - echo '{optional}' - OK"}, 200
            case _:
                return {"message": f"{operation}: Invalid operation"}, 404

    def post(self, operation, optional=None):
        """Relay control and status"""
        match operation:
            case "login":
                hp_api.login()
                return {"message": "Login successful"}
            case "refresh_basic_info":
                hp_api.update_heat_pump_basic_information()
                return {"message": "Refresh successful"}
            case _:
                return {"message": f"{operation}: Invalid operation"}, 404


class RelayControllerVersion(Resource):
    def get(self):
        """Return current version"""
        return {"version": __version__}


## Actually set up the API resource routing here
api.add_resource(HPInfo, "/hp_info/<string:about>", "/hp_info/<string:about>/<int:heating_loop>")
api.add_resource(HPController, "/hp_control/<string:operation>")

api.add_resource(RelayControllerVersion, "/version")
api.add_resource(RelayController, "/relay/<string:operation>/", "/relay/<string:operation>/<optional>")


if __name__ == "__main__":
    app.run()
