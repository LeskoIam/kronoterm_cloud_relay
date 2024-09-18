__version__ = "0.0.3"

import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api, Resource, reqparse
from kronoterm_cloud_api import KronotermCloudApi
from kronoterm_enums import HeatingLoop, HeatingLoopMode, WorkingFunction

from src.util.logz import create_logger

log = create_logger(__name__)

load_dotenv()

hp_api = KronotermCloudApi(username=os.getenv("KRONOTERM_CLOUD_USER"), password=os.getenv("KRONOTERM_CLOUD_PASSWORD"))
hp_api.login()
hp_api.update_heat_pump_basic_information()

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


def info_summary():
    """Heating loop 2 summary.

    :return: summary for heating loop 2
    """
    system_review_data = hp_api.get_system_review_data()
    loop_1_data = hp_api.get_heating_loop_data(HeatingLoop.HEATING_LOOP_1)
    loop_2_data = hp_api.get_heating_loop_data(HeatingLoop.HEATING_LOOP_2)
    alarms_data = hp_api.get_alarms_data()["AlarmsData"]

    room_temperature = system_review_data["TemperaturesAndConfig"]["heating_circle_2_temp"]
    outlet_temperature = system_review_data["CurrentFunctionData"][0]["dv_temp"]
    outside_temperature = system_review_data["TemperaturesAndConfig"]["outside_temp"]
    sanitary_water_temperature = system_review_data["TemperaturesAndConfig"]["tap_water_temp"]
    working_function = system_review_data["TemperaturesAndConfig"]["working_function"]

    heating_loop_1_target_temp = loop_1_data["HeatingCircleData"]["circle_temp"]
    heating_loop_1_working_status = loop_1_data["HeatingCircleData"]["circle_status"]
    heating_loop_1_working_mode = loop_1_data["HeatingCircleData"]["circle_mode"]

    heating_loop_2_target_temp = loop_2_data["HeatingCircleData"]["circle_temp"]
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
            "working_function": WorkingFunction(working_function).name,
        },
        "heating_loop_1": {
            "heating_loop_1_target_temp": heating_loop_1_target_temp,
            "heating_loop_1_working_status": heating_loop_1_working_status,
            "heating_loop_1_working_mode": HeatingLoopMode(heating_loop_1_working_mode).name,
        },
        "heating_loop_2": {
            "heating_loop_2_target_temp": heating_loop_2_target_temp,
            "heating_loop_2_working_status": heating_loop_2_working_status,
            "heating_loop_2_working_mode": HeatingLoopMode(heating_loop_2_working_mode).name,
        },
    }
    return output


class HPInfo(Resource):
    def get(self, about):  # noqa: C901
        """Get heat pump data based on `about` argument"""
        match about:
            case "info_summary":
                return info_summary()
            case "heat_loop_2":
                return {"data": hp_api.get_heating_loop_data(HeatingLoop.HEATING_LOOP_2)}
            case "system_review":
                return {"data": hp_api.get_system_review_data()}
            case "target_temperature":
                return {"data": hp_api.get_heating_loop_target_temperature(HeatingLoop.HEATING_LOOP_2)}
            case "room_temperature":
                return {"data": hp_api.get_room_temp()}
            case "outside_temperature":
                return {"data": hp_api.get_outside_temperature()}
            case "outlet_temperature":
                return {"data": hp_api.get_outlet_temp()}
            case "working_function":
                return {"data": hp_api.get_working_function().name}
            case "working_status":
                return {"data": hp_api.get_heating_loop_status(HeatingLoop.HEATING_LOOP_2)}
            case "working_mode":
                return {"data": hp_api.get_heating_loop_mode(HeatingLoop.HEATING_LOOP_2).name}
            case "water_temperature":
                return {"data": hp_api.get_sanitary_water_temp()}
            case _:
                return f"about/{about} not supported", 404


parser.add_argument("temperature", type=float)
parser.add_argument("mode", type=str)
# HeatingLoop.HEATING_LOOP_1 = 1
# HeatingLoop.HEATING_LOOP_2 = 2
# HeatingLoop.TAP_WATER = 3
parser.add_argument("heating_loop", type=int)


class HPController(Resource):
    def post(self, operation):
        """Set heat pump temperature and operation mode"""
        args = parser.parse_args()
        heating_loop = args.get("heating_loop")
        if heating_loop not in HeatingLoop:
            return {"message": f"Heating loop '{heating_loop}' not supported"}, 404
        heating_loop = HeatingLoop(heating_loop)
        match operation:
            case "set_target_temperature":
                temp = args.get("temperature")
                if temp is not None:
                    hp_api.set_heating_loop_target_temperature(heating_loop, temp)
                    return_message = {"message": f"Set temperature of '{heating_loop.name}' to {temp} degrees Celsius"}
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
                    return_message = {"message": f"Set heating loop {heating_loop.name} mode to {mode}"}
                else:
                    return {"message": "'mode' not set"}, 404
            case _:
                return {"message": f"'{operation}': Invalid operation"}, 404
        return return_message, 200


class RelayController(Resource):
    def get(self, operation):
        """Healthcheck endpoint"""
        return_message = {"message": f"relay - echo '{operation}' - OK"}
        return return_message, 200

    def post(self, operation):
        """Relay control and status"""
        match operation:
            case "login":
                hp_api.login()
                return_message = {"message": "Login successful"}
            case _:
                return {"message": f"{operation}: Invalid operation"}, 404

        return return_message, 200


class RelayControllerVersion(Resource):
    def get(self):
        """Return current version"""
        return_message = {"version": __version__}
        return return_message, 200


## Actually set up the API resource routing here
api.add_resource(HPInfo, "/hp-info/<about>")
api.add_resource(HPController, "/hp-control/<operation>")

api.add_resource(RelayControllerVersion, "/version")
api.add_resource(RelayController, "/relay/<operation>")


if __name__ == "__main__":
    app.run(debug=True)
