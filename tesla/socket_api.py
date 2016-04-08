from app import socketio
from flask.ext.socketio import emit

from models import vehicles, tokens

#Clean up / replace with Victors "Garage" stuff.
def find_user_vehicles(email):
    for id, token in tokens.items():
        if token['email'] == email:
            print('found user ', email)
            vehicles = None
            try:
                my_vehicles = info['vehicles']
            except KeyError:
                my_vehicles = vehicles.find_vehicle(info['email'])
                token['vehicles'] = my_vehicles

            print('find_user_vehicles: ', my_vehicles)
            return my_vehicles

    return None

def find_all_vehicles():
    return  vehicles.find_all_vehicles()

@socketio.on('list_vehicle_ids')
def list_vehicle_ids(params):
    print('list_vehicle_ids ', params)

    message = {}

    if params and params['email']:
        message['email'] = params['email'],
        my_vehicles = find_user_vehicles(params['email'])
    else:
        my_vehicles = find_all_vehicles()

    vehicle_ids = []
    if my_vehicles is not None:
    	for vehicle in my_vehicles:
        	vehicle_ids.append(vehicle)

    message['response'] = {
        "vehicle_ids": vehicle_ids
    }

    print('list_vehicle_ids result', message)

    emit('list_vehicle_ids', message)

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
