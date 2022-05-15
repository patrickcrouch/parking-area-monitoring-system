import simpy

class ParkingLot:
    def __init__(self, env, spaces, lot_number, label, first_choice_probability):
        self.parking_spaces = simpy.Resource(env, spaces)
        self.lot_number = lot_number
        self.probability = first_choice_probability
        self.label = label