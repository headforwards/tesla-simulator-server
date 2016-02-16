import random
import re

from flask import request, make_response, jsonify, Blueprint, current_app as app

tokens = {}
vehicles = []
blue_api = Blueprint('api', __name__)


def get_random_string():
    return 'test'


@blue_api.route('/oauth/token', methods=['POST'])
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


@blue_api.route('/vehicles/<vehicle_id>/command/honk_horn', methods=['POST'])
def honk_horn(vehicle_id):
    try:
        info = find_user(request)

        find_vehicle(vehicle_id, info)
        app.socketio.send({ 'command': 'honk_horn', 'vehicle_id': vehicle_id }, json=True);
        return jsonify({
          "response": {
            "result": True,
            "reason": ""
          }
        })

    except KeyError:
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)
