from app import socketio
from flask.ext.socketio import emit

from models import vehicles, tokens

#Clean up / replace with Victors "Garage" stuff.
def find_user_vehicles(email):
    for id, token in tokens.items():
        if token['email'] == email:
            print('found user ', email)
            vehicles = None
            if token['vehicles']:
                print('vehicles: ', token['vehicles'])
                vehicles = []
                for vehicle in token['vehicles']:
                    vehicles.append(vehicle.vehicle_id)
            return vehicles

    return None

@socketio.on('list_vehicle_ids')
def list_vehicle_ids(params):
    print('list_vehicle_ids ', params)

    vechicles_result = None;
    message = {}

    if params and params['email']:
        message['email'] = params['email'],
        vechicles_result = find_user_vehicles(params['email'])
    else:
        vechicles_result = vehicles

    message['response'] = {
        "vehicle_ids": vechicles_result
    }

    print('list_vehicle_ids result', message)

    emit('list_vehicle_ids', message)

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
