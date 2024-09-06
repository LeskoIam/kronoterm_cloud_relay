import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api, Resource, reqparse
from hp_enums import HeatingLoopMode
from kronoterm_cloud_api import HeatingLoop, KronotermCloudApi

load_dotenv()

hp_api = KronotermCloudApi(username=os.getenv("KRONOTERM_CLOUD_USER"), password=os.getenv("KRONOTERM_CLOUD_PASSWORD"))
hp_api.login()

app = Flask(__name__)
api = Api(app)

# def abort_if_todo_doesnt_exist(todo_id):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument("temperature", type=float)
parser.add_argument("mode", type=str)


class HPInfo(Resource):
    def get(self, about):
        """Get heat pump data based on `about` argument"""
        match about:
            case "general":
                return {"data": hp_api.get_circle_2()}
            case "set_temperature":
                return {"data": hp_api.get_heating_loop_set_temperature(HeatingLoop.LOW_TEMPERATURE_LOOP)}
            case "room_temperature":
                return {"data": hp_api.get_room_temp()}
            case "outside_temperature":
                return {"data": hp_api.get_outside_temperature()}
            case "outlet_temperature":
                return {"data": hp_api.get_outlet_temp()}
            case "working_function":
                return {"data": hp_api.get_working_function().name}
            case "working_status":
                return {"data": hp_api.get_working_status()}
            case "water_temperature":
                return {"data": hp_api.get_sanitary_water_temp()}
            case _:
                return f"about/{about} not supported", 404


class HPController(Resource):
    def post(self, operation):
        """Set heat pump temperature and operation mode"""
        args = parser.parse_args()
        print(args)
        print(operation)
        match operation:
            case "set_temperature":
                temp = args.get("temperature")
                if temp is not None:
                    hp_api.set_heating_loop_temperature(HeatingLoop.LOW_TEMPERATURE_LOOP, temp)
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
    def post(self, operation):
        """Relay control and status"""
        print(operation)
        match operation:
            case "echo":
                return_message = {"message": operation}
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
