__version__ = "0.0.2"

import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api, Resource, reqparse
from kronoterm_cloud_api import KronotermCloudApi
from kronoterm_enums import HeatingLoop, HeatingLoopMode, WorkingFunction

load_dotenv()

hp_api = KronotermCloudApi(username=os.getenv("KRONOTERM_CLOUD_USER"), password=os.getenv("KRONOTERM_CLOUD_PASSWORD"))
hp_api.login()

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("temperature", type=float)
parser.add_argument("mode", type=str)


def info_summary():
    """Heating loop 2 summary.

    :return: summary for heating loop 2
    """
    system_review_data = hp_api.get_system_review_data()
    low_temp_loop_data = hp_api.get_heating_loop_data(HeatingLoop.LOW_TEMPERATURE_LOOP)

    room_temperature = system_review_data["TemperaturesAndConfig"]["heating_circle_2_temp"]
    outlet_temperature = system_review_data["CurrentFunctionData"][0]["dv_temp"]
    low_temp_target_temp = low_temp_loop_data["HeatingCircleData"]["circle_temp"]
    outside_temperature = system_review_data["TemperaturesAndConfig"]["outside_temp"]
    sanitary_water_temperature = system_review_data["TemperaturesAndConfig"]["tap_water_temp"]
    working_function = system_review_data["TemperaturesAndConfig"]["working_function"]
    working_status = low_temp_loop_data["HeatingCircleData"]["circle_status"]
    working_mode = low_temp_loop_data["HeatingCircleData"]["circle_mode"]

    output = {
        "room_temperature": room_temperature,
        "outside_temperature": outside_temperature,
        "sanitary_water_temperature": sanitary_water_temperature,
        "outlet_temperature": outlet_temperature,
        "low_temp_target_temp": low_temp_target_temp,
        "working_function": WorkingFunction(working_function).name,
        "working_status": working_status,
        "working_mode": HeatingLoopMode(working_mode).name,
    }
    return output


class HPInfo(Resource):
    def get(self, about):  # noqa: C901
        """Get heat pump data based on `about` argument"""
        match about:
            case "info_summary":
                return info_summary()
            case "heat_loop_2":
                return {"data": hp_api.get_heating_loop_data(HeatingLoop.LOW_TEMPERATURE_LOOP)}
            case "system_review":
                return {"data": hp_api.get_system_review_data()}
            case "set_temperature":
                return {"data": hp_api.get_heating_loop_target_temperature(HeatingLoop.LOW_TEMPERATURE_LOOP)}
            case "room_temperature":
                return {"data": hp_api.get_room_temp()}
            case "outside_temperature":
                return {"data": hp_api.get_outside_temperature()}
            case "outlet_temperature":
                return {"data": hp_api.get_outlet_temp()}
            case "working_function":
                return {"data": hp_api.get_working_function().name}
            case "working_status":
                return {"data": hp_api.get_heating_loop_working_status(HeatingLoop.LOW_TEMPERATURE_LOOP)}
            case "working_mode":
                return {"data": hp_api.get_heating_loop_mode(HeatingLoop.LOW_TEMPERATURE_LOOP).name}
            case "water_temperature":
                return {"data": hp_api.get_sanitary_water_temp()}
            case _:
                return f"about/{about} not supported", 404


class HPController(Resource):
    def post(self, operation):
        """Set heat pump temperature and operation mode"""
        args = parser.parse_args()
        match operation:
            case "set_temperature":
                temp = args.get("temperature")
                if temp is not None:
                    hp_api.set_heating_loop_target_temperature(HeatingLoop.LOW_TEMPERATURE_LOOP, temp)
                    return_message = {"message": f"Set temperature to {temp} degrees Celsius"}
                else:
                    return_message = {"message": "set-temperature arg/s missing"}

            case "set_heating_loop_mode":
                mode = args.get("mode").upper()
                if mode is not None:
                    mode = mode.upper()
                    return_message = {"message": f"Set mode to {mode}"}
                    if mode == "ON":
                        hp_api.set_heating_loop_mode(HeatingLoop.LOW_TEMPERATURE_LOOP, HeatingLoopMode.ON)
                    elif mode == "OFF":
                        hp_api.set_heating_loop_mode(HeatingLoop.LOW_TEMPERATURE_LOOP, HeatingLoopMode.OFF)
                    elif mode == "AUTO":
                        hp_api.set_heating_loop_mode(HeatingLoop.LOW_TEMPERATURE_LOOP, HeatingLoopMode.AUTO)
                    else:
                        return_message = {"message": f"Invalid mode {mode}"}
                else:
                    return_message = {"message": "set-heating-loop-mode arg/s missing"}
            case _:
                return_message = {"message": f"{operation}: Invalid operation"}
        return return_message, 200


class RelayController(Resource):
    def get(self, operation):
        return_message = {"message": f"relay - echo '{operation}' - OK"}
        return return_message, 200

    def post(self, operation):
        """Relay control and status"""
        match operation:
            case "login":
                hp_api.login()
                return_message = {"message": "Login successful"}
            case _:
                return_message = {"message": f"{operation}: Invalid operation"}

        return return_message, 200


##
## Actually setup the Api resource routing here
##
api.add_resource(HPInfo, "/hp-info/<about>")
api.add_resource(RelayController, "/relay/<operation>")
api.add_resource(HPController, "/hp-control/<operation>")


if __name__ == "__main__":
    app.run(debug=True)
