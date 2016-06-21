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
    'set_temps': {'driver_temp': float, 'passenger_temp': float},
    'sun_roof_control': {'state': str, 'percent': int},
    'trunk_open': {'which_trunk': str},
}

def validate_command(func):
    @wraps(func)
    def wrapper(vehicle_id, command):
        try:
            if command not in valid_commands:
                abort(404)

            # FIXME Add all form args to kwargs
            command_kwargs = {}

            if valid_commands[command]:
                for expected_arg, type in valid_commands[command].items():
                    arg = request.form[expected_arg]

                    if not isinstance(arg, type):
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
@validate_command
def handle_command(vehicle_id, command, command_kwargs=None):

    info = find_user(request)
    vehicle = vehicles[vehicle_id]

    print('vehicle', vehicle, 'info', info,
        'command_kwargs', command_kwargs)

    if vehicle.get_user_id() != info['email']:
        abort(401)

    method = getattr(vehicle, command, None)

    # FIXME Add support for optional arguments (#95)
    if method:
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
  'drive_state',
  'vehicle_state',
  # 'gui_settings',
  # 'mobile_enabled',
)

@blue_api.route('/vehicles/<vehicle_id>/data_request/<request_type>', methods=['GET'])
def handle_requests(vehicle_id, request_type):
    try:
        info = find_user(request)
        vehicle = vehicles[vehicle_id]

        if vehicle.get_user_id() != info['email']:
            abort(401)

        if request_type not in valid_requests:
          abort(404);

        method = getattr(vehicle, 'get_' + request_type, None)

        return jsonify({
          "response": method()
        })

    except KeyError:
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)
