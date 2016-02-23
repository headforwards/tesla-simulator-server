#!/usr/bin/env python
from app import create_app
from flask.ext.socketio import emit

from flask import jsonify

app = create_app()

@app.socketio.on('json')
def test_message(json):
    print('json ', json)
    #use try !
    vehicle_ids = ('test',)
    #if json.command and json.command == 'list_vehicle_ids':
      # if json.email:
      #     find vehicles belonging to user
      # else:
      #     return all vehicles.
    message = {
      "command": "list_vehicle_ids",
      #"email": json['email'],
      "response": {
          "vehicle_ids": vehicle_ids
      }
    }
    emit('json', message)

@app.socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@app.socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    app.socketio.run(
        app,
        debug=app.config['DEBUG'],
        port=app.config['PORT']
    )
