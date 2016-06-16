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
    if isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, TeslaVehicle):
        return repr(obj)
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
        self.password = None
        self.valet_mode = __OFF__
        self.charging = __OFF__
        self.door_locked = __OFF__
        self.charge_port_door = __OFF__
        self.charge_mode = 90
        self.havc_system = __ON__
        self.passenger_temp = 18.0
        self.driver_temp = 18.0
        self.vehicle_id = vehicle_id or str(uuid.uuid4())

    def __repr__(self):
        return self.status

    @property
    def status(self):
        return json.dumps(self.__dict__)

    def hork_horn(self):
        return self.status

    def switch_lights(self, action):
        self.lights = action
        return self.status

    def reset_valet_pin (self):
        self.password = None

    def set_valet_mode(self, on, password=None):
        self.password = password if password else self.password
        # FIXME == True when (api.js 122)
        self.valet_mode = __ON__ if on == True else __OFF__

    def charge_start(self):
        self.charging = __ON__

    def charge_stop(self):
        self.charging = __OFF__

    def door_lock(self):
        self.door_locked = __ON__

    def door_unlock(self):
        self.door_locked = __OFF__

    def auto_conditioning_start(self):
        self.havc_system = __ON__

    def auto_conditioning_stop(self):
        self.havc_system = __OFF__

    def charge_port_door_open(self):
        self.charge_port_door = __ON__

    def charge_standard(self):
        self.charge_mode = 90

    def charge_max_range(self):
        self.charge_mode = 100

    def charge_limit(self, charge):
        self.charge_mode = charge

    def remote_start_drive(self, password):
        # The password to the authenticated
        # my.teslamotors.com account.
        self.state = 'running'

    def set_temps(self, driver_temp, passenger_temp):
        self.passenger_temp = passenger_temp
        self.driver_temp = driver_temp

    def set_user(self, user_id):
        self.user_id = user_id
        return self.status

    def get_user_id(self):
        return self.user_id

    def get_vehicle_id(self):
        return self.vehicle_id


class Vehicles(object):
    _VEHICLES = {}

    def __getitem__(self, vehicle_id):
        return self._VEHICLES[vehicle_id]

    def __len__(self):
        return len(self._VEHICLES)

    def create_vehicle(self, name, user_id=None):
        vehicle = TeslaVehicle(name, user_id, choice(__COLOR__))
        self._VEHICLES[str(vehicle.vehicle_id)] = vehicle
        return vehicle

    def find_vehicles(self, user_id):
        vehicles = list(filter(lambda x: x[1].get_user_id() == user_id,
            self._VEHICLES.items()))

        if not vehicles:
            self.create_vehicle('my vehicle', user_id)
            vehicles = self.find_vehicles(user_id)
        return vehicles

    def find_all_vehicles(self):
        return self._VEHICLES

vehicles = Vehicles()
tokens = {}
