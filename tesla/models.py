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
        # FIXME Add data store for vehicle state
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
        self.sun_roof_percent = 0
        self.is_frunk_open = False
        self.is_trunk_open = False
        self.vehicle_id = vehicle_id or str(uuid.uuid4())

        self.climate_state = {
            "inside_temp": 17.0,
            "outside_temp": 9.5,
            "driver_temp_setting": 22.6,
            "passenger_temp_setting": 22.6,
            "is_auto_conditioning_on": False,
            "is_front_defroster_on": None,
            "is_rear_defroster_on": False,
            "fan_status": 0,
        }

        self.charge_state = {
            "charging_state": "Complete",
            "charge_to_max_range": False,
            "max_range_charge_counter": 0,
            "fast_charger_present": False,
            "battery_range": 239.02,
            "est_battery_range": 155.79,
            "ideal_battery_range": 275.09,
            "battery_level": 91,
            "battery_current": -0.6,
            "charge_starting_range": None,
            "charge_starting_soc": None,
            "charger_voltage": 0,
            "charger_pilot_current": 40,
            "charger_actual_current": 0,
            "charger_power": 0,
            "time_to_full_charge": None,
            "charge_rate": -1.0,
            "charge_port_door_open": True,
        }

        self.drive_state = {
            "shift_state": None,
            "speed": None,
            "latitude": 33.794839,
            "longitude": -84.401593,
            "heading": 4,
            "gps_as_of": 1359863204,
        }

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
        return self.status

    def set_valet_mode(self, on, password=None):
        self.password = password if password else self.password
        self.valet_mode = __ON__ if on == True else __OFF__
        return self.status

    def charge_start(self):
        self.charging = __ON__
        return self.status

    def charge_stop(self):
        self.charging = __OFF__
        return self.status

    def door_lock(self):
        self.door_locked = __ON__
        return self.status

    def door_unlock(self):
        self.door_locked = __OFF__
        return self.status

    def auto_conditioning_start(self):
        self.havc_system = __ON__
        return self.status

    def auto_conditioning_stop(self):
        self.havc_system = __OFF__
        return self.status

    def charge_port_door_open(self):
        self.charge_port_door = __ON__
        return self.status

    def charge_standard(self):
        self.charge_state.charge_to_max_range = False
        return self.status

    def charge_max_range(self):
        self.charge_state.charge_to_max_range = True
        return self.status

    def charge_limit(self, charge):
        self.charge_state.charger_power = charge
        return self.status

    def sun_roof_control(self, state, percent=None):
        if(state == 'move'):
            self.sun_roof_percent = percent
        elif (state == 'open'):
            self.sun_roof_percent = 100
        elif (state == 'close'):
            self.sun_roof_percent = 0
        elif (state == 'comfort'):
            self.sun_roof_percent = 80
        elif (state == 'vent'):
            self.sun_roof_percent = 20

        return self.status

    def trunk_open(which_trunk):
        if(which_trunk == 'rear'):
            self.is_trunk_open = True
        elif(which_trunk == 'rear'):
            self.is_frunk_open = True

        return self.status

    def remote_start_drive(self, password):
        # The password to the authenticated
        # my.teslamotors.com account.
        self.state = 'running'
        return self.status

    def set_temps(self, driver_temp, passenger_temp):
        self.climate_state.passenger_temp_setting = passenger_temp
        self.climate_state.driver_temp_setting = driver_temp
        return self.status

    def set_user(self, user_id):
        self.user_id = user_id
        return self.status

    def get_user_id(self):
        return self.user_id

    def get_vehicle_id(self):
        return self.vehicle_id

    def get_charge_state(self):
        return self.charge_state

    def get_drive_state(self):
        return self.drive_state

    def get_climate_state(self):
        return self.climate_state

    def get_vehicle_state(self):
        return self.state

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
