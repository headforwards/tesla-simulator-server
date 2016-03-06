"""
Tesla car model
"""
import uuid
import json
from random import choice

__OFF__ = 'off'
__ON__ = 'on'
__COLOR__ = ['black', 'white', 'red', 'brown', 'gold', 'pink']
JSONEncoder_old = json.JSONEncoder.default


def JSONEncoder_new(self, obj):
    if isinstance(obj, uuid.UUID): return str(obj)
    return JSONEncoder_old(self, obj)
json.JSONEncoder.default = JSONEncoder_new


class TeslaVehicle(object):
    def __init__(self, name, user_id, color, vehicle_id=None):
        self.color = color
        self.display_name = name
        self.state = 'online'
        self.user_id = user_id
        self.lights = __OFF__
        self.horn = __OFF__
        self.vehicle_id = vehicle_id or uuid.uuid4()

    def __repr__(self):
        return self.status

    @property
    def status(self):
        return json.dumps(self.__dict__)

    def hork_horn(self):
        return self.status

    def switch_lights(self, action):
        # if action not in [__OFF__, __ON__]: exception
        self.lights = action
        return self.status

    def set_user(self, user_id):
        self.user_id = user_id
        return self.status


class Vehicles(object):
    _VEHICLES = {}

    def __init__(self):
        self.create_vehicle('Tesla1')

    def __getitem__(self, vehicle_id):
        return self._VEHICLES[vehicle_id]

    def __len__(self):
        return len(self._VEHICLES)

    def create_vehicle(self, name, user_id=None):
        vehicle = TeslaVehicle(name, user_id, choice(__COLOR__))
        self._VEHICLES[str(vehicle.vehicle_id)] = vehicle
        return vehicle


vehicles = Vehicles()
