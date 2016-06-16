import uuid
import re

from flask import request, make_response, jsonify, json, abort, Blueprint, current_app as app
from models import vehicles, tokens
from functools import wraps

blue_api = Blueprint('api', __name__)
auth_api = Blueprint('oauth', __name__)

def get_random_string():
    return str(uuid.uuid4())

#This doesn't have an /api/1 prefix!
@auth_api.route('/oauth/token', methods=['POST'])
def oauth_token():
    if request.form and request.form['email']:
        #Create session
        token = get_random_string()
        tokens[token] = {
            "email": request.form['email']
        }

        return jsonify({
          "access_token": token,
          "token_type": "bearer",
          "expires_in": -1 #FIXME
        })
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


def find_user(request):
    token = re.sub(r'Bearer {([^}]+)}',
            '\g<1>',
            request.headers['Authorization'])

    print('find_user ', token)
    return tokens[token]


@blue_api.route('/vehicles', methods=['GET'])
def get_vehicles():

    try:
        info = find_user(request)
    except KeyError:
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)

    my_vehicles = vehicles.find_vehicles(info['email'])
    print ('my_vehicles', my_vehicles)

    return jsonify({
        "response": [veh[1].__dict__ for veh in my_vehicles],
        "count": len(my_vehicles)
    })


def find_vehicle(vehicle_id, info):

    print(tokens)
    print("Vehicle id ", vehicle_id)
    if info['vehicles'][0].vehicle_id == vehicle_id:
        return info['vehicles'][0].vehicle_id
    raise KeyError('No vehicle_id matching ', vehicle_id, ' for this user')


valid_commands = {
    'honk_horn': None,
    'lights_on': None,
    'lights_off': None,
    'flash_lights': None,
    'wake_up': None,
    'charge_start': None,
    'charge_stop': None,
    'charge_port_door_open': None,
    'charge_standard': None,
    'charge_max_range': None,
    'door_unlock': None,
    'door_lock': None,
    'auto_conditioning_start': None,
    'auto_conditioning_stop': None,
    'set_valet_mode': {'on': bool, 'password': str},
    'reset_valet_pin': None,
    'set_charge_limit': {'percent': int},
    'remote_start_drive': {'password': str},
    'set_temps': {'driver_temp': float, 'passenger_temp': float}
}

# 'sun_roof_control': {state: state})
# 'sun_roof_control': {state: "move", percent: percent})
# 'trunk_open': {which_trunk: "rear"})
# 'trunk_open': {which_trunk: "front"})

def validate_json(func):

    @wraps(func)
    def wrapper(vehicle_id, command):
        try:
            if not command in list(valid_commands.keys()):
                abort(404)

            command_kwargs = {}

            if valid_commands[command] != None:
                for expected_arg, type in valid_commands[command].items():
                    arg = request.form[expected_arg]

                    if (not isinstance(arg, type)):
                        try:
                            arg = json.loads(arg)
                        except KeyError:
                            return make_response(jsonify({
                                'error': 'Bad Request'
                            }), 400)

                    if isinstance(arg, type) == False:
                        abort(403)

                    command_kwargs[expected_arg] = arg

            return func(vehicle_id, command, command_kwargs)

        except KeyError:
            return make_response(jsonify({
                'error': 'Unauthorized access'
            }), 403)

    return wrapper

@blue_api.route('/vehicles/<vehicle_id>/command/<command>', methods=['POST'])
@validate_json
def handle_command(vehicle_id, command, command_kwargs=None):

    info = find_user(request)
    vehicle = vehicles[vehicle_id]

    print('vehicle', vehicle, 'info', info,
        'command_kwargs', command_kwargs)

    if vehicle.get_user_id() != info['email']:
        abort(401)

    method = getattr(vehicle, command, None)

    if(method != None):
        method(**command_kwargs)

    return send_reply(vehicle_id, command)


def send_reply(vehicle_id, command):
    app.socketio.send({
        'command': command,
        'vehicle_id': vehicle_id
    }, json=True)

    return jsonify({
        "response": {
            "result": True,
            "reason": ""
        }
    })


valid_requests = (
  'charge_state',
  'climate_state',
  # 'drive_state',
  # 'vehicle_state',
  # 'gui_settings',
  # 'mobile_enabled',
)

responses = {
  'charge_state': {
    "charging_state": "Complete",  # "Charging", ??
    "charge_to_max_range": False,  # current std/max-range setting
    "max_range_charge_counter": 0,
    "fast_charger_present": False, # connected to Supercharger?
    "battery_range": 239.02,       # rated miles
    "est_battery_range": 155.79,   # range estimated from recent driving
    "ideal_battery_range": 275.09, # ideal miles
    "battery_level": 91,           # integer charge percentage
    "battery_current": -0.6,       # current flowing into battery
    "charge_starting_range": None,
    "charge_starting_soc": None,
    "charger_voltage": 0,          # only has value while charging
    "charger_pilot_current": 40,   # max current allowed by charger & adapter
    "charger_actual_current": 0,   # current actually being drawn
    "charger_power": 0,            # kW (rounded down) of charger
    "time_to_full_charge": None,   # valid only while charging
    "charge_rate": -1.0,           # float mi/hr charging or -1 if not charging
    "charge_port_door_open": True
  },

  'climate_state': {
    "inside_temp": 17.0,          # degC inside car
    "outside_temp": 9.5,          # degC outside car or None
    "driver_temp_setting": 22.6,  # degC of driver temperature setpoint
    "passenger_temp_setting": 22.6, # degC of passenger temperature setpoint
    "is_auto_conditioning_on": False, # apparently even if on
    "is_front_defroster_on": None, # None or boolean as integer?
    "is_rear_defroster_on": False,
    "fan_status": 0               # fan speed 0-6 or None
  },

  'drive_state': {
    "shift_state": None,          #
    "speed": None,                #
    "latitude": 33.794839,        # degrees N of equator
    "longitude": -84.401593,      # degrees W of the prime meridian
    "heading": 4,                 # integer compass heading, 0-359
    "gps_as_of": 1359863204       # Unix timestamp of GPS fix
  }
}

@blue_api.route('/vehicles/<vehicle_id>/data_request/<request_type>', methods=['GET'])
def handle_requests(vehicle_id, request_type):
    try:
        info = find_user(request)

        find_vehicle(vehicle_id, info)

        if not request_type in responses:
          abort(404);

        return jsonify({
          "response": responses[request_type]
        })

    except KeyError:
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)
