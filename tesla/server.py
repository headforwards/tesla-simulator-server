#!/usr/bin/env python

from flask import Flask, session, request, make_response, jsonify
import os
import random
import string
import re

def get_random_string():
    return 'test'
    #return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])

class Config(object):
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = os.getenv('TESLA_PORT', 8000)
    #http://docs.timdorr.apiary.io/#reference/authentication/tokens
    # TESLA_CLIENT_ID=e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e
    # TESLA_CLIENT_SECRET=c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220

app = Flask(__name__)

#Not using sessions - we are returning an access_token, store a dictionary of
#these as keys to vehicle data, etc.
tokens = {}

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/oauth/token', methods=['POST'])
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

@app.route('/api/1/vehicles', methods=['GET'])
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

@app.route('/api/1/vehicles/<vehicle_id>/command/honk_horn', methods=['POST'])
def honk_horn(vehicle_id):
    try: 
        info = find_user(request)

        find_vehicle(vehicle_id, info)

        return jsonify({
          "response": {
            "result": True,
            "reason": ""
          }
        })

    except KeyError:
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    

def main():
    app.secret_key = '\xc85\x95\x9a\x80\xc1\x93\xd0\xe9\x95\x08\xfb\xbe\x85\xd0\x1aq\xd3\x95\xc9\xad \xc0\x08'
    app.run(debug=Config.DEBUG, port=Config.PORT)

if __name__ == '__main__':
    main()
