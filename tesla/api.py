import uuid
import re

from flask import request, make_response, jsonify, abort, Blueprint, current_app as app
from vehicles import vehicles, tokens

blue_api = Blueprint('api', __name__)
auth_api = Blueprint('oauth', __name__)

def get_random_string():
    return str(uuid.uuid4())
    #return 'test'

#This doesn't have an /api/1 prefix!
@auth_api.route('/oauth/token', methods=['POST'])
def oauth_token():
    if request.form and request.form['email']:
        #Create session
        token = get_random_string();
        tokens[token] = {
            "email": request.form['email']
        }
        #session['email'] = request.form['email'],
        return jsonify({
          "access_token": token,
          "token_type": "bearer",
          "expires_in": -1 #FIXME
        })
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


def find_user(request):
    token = re.sub(r'Bearer {([^}]+)}',
            '\g<1>',
            request.headers['Authorization']
            )

    print 'find_user ', token
    print tokens
    return tokens[token]


@blue_api.route('/vehicles', methods=['GET'])
def get_vehicles():
    #check bearer token
    #check session for vehicle list
        #create if not exist
    #return vehicle id, etc
    print tokens
    try:
        info = find_user(request)
    except KeyError:
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    try:
        vehicle_id = info['vehicles'][0]["vehicle_id"]
    except KeyError:
        vehicle_id = get_random_string();
        info['vehicles'] = [ { "vehicle_id": vehicle_id }]
        vehicles.append(vehicle_id);

    return jsonify({"response": [{
          "color": "red",
          "display_name": "my car",
          "id": 321,
          "option_codes": "MS01,RENA,TM00,DRLH,PF00,BT85,PBCW,RFPO,WT19,IBMB,IDPB,TR00,SU01,SC01,TP01,AU01,CH00,HP00,PA00,PS00,AD02,X020,X025,X001,X003,X007,X011,X013",
          "user_id": 123,
          "vehicle_id": vehicle_id,
          "vin": "5YJSA1CN5CFP01657",
          "tokens": [
            "x",
            "x"
          ],
          "state": "online"
        }
      ],
      "count": 1
    })


def find_vehicle(vehicle_id, info):
    print tokens
    print "Vehicle id ", vehicle_id
    if info['vehicles'][0]['vehicle_id'] == vehicle_id:
        return info['vehicles'][0]['vehicle_id']
    raise KeyError('No vehicle_id matching ', vehicle_id, ' for this user')


valid_commands = (
  'honk_horn',
  'lights_on',
  'lights_off'
)
@blue_api.route('/vehicles/<vehicle_id>/command/<command>', methods=['POST'])
def handle_command(vehicle_id, command):
    try:
        info = find_user(request)

        find_vehicle(vehicle_id, info)

        if not command in valid_commands:
          abort(404);

        app.socketio.send({ 'command': command, 'vehicle_id': vehicle_id }, json=True);
        return jsonify({
          "response": {
            "result": True,
            "reason": ""
          }
        })

    except KeyError:
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)


valid_requests = (
  'charge_state',
  'climate_state',
  #'drive_state'
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
