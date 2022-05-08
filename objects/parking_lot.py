import simpy
import random

class ParkingLot:
    def __init__(self, env, capacity, lot_number, label):
        self.parking_spaces = simpy.Resource(env, capacity)
        self.lot_number = lot_number
        self.label = label