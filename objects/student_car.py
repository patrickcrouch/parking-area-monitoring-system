from numpy import random
from itertools import cycle

class StudentCar(object):

    def __init__(self, env, label, parking_lots):
        self.env = env
        # car label
        self.label = label
        # Max minutes to wait in a single lot
        self.single_lot_patience = random.triangular(5.0, 15.0, 25.0)
        # Time needed in lot
        self.park_time_required = random.triangular(60.0, 180.0, 360.0)
        # randomized lot preference order
        self.lot_preference = parking_lots.copy()
        random.shuffle(self.lot_preference)
        # Total wait time experienced
        self.wait_time = 0.0
        self.lot_visits = 0
        self.parked = False
        

    def park(self, env, student_car_data, lot_full_enabled=False):
        # Get first lot preference
        arrival_time = env.now
        for lot in cycle(self.lot_preference):
            # start
            # break the loop and leave if total patience exceeded
            with lot.parking_spaces.request() as got_parking:
                parking_attempt = yield got_parking | env.timeout(self.single_lot_patience, 2)
                # Got a parking space
                if got_parking in parking_attempt:
                    self.wait_time = env.now - arrival_time
                    self.lot_visits += 1
                    self.parked = True
                    yield env.timeout(self.park_time_required)
                    break
                elif 2 in parking_attempt.values():
                    self.lot_visits += 1
                    self.parked = False
                    continue
                else:
                    print('Something not caught: {}'.format(parking_attempt))
        # put excel line data for individual car stats here
        student_car_data[self.label] = [self.wait_time, self.single_lot_patience, self.park_time_required, self.lot_preference, self.lot_visits]
        if self.parked == False:
            print('{}, {}, {}, {}'.format(self.wait_time, self.single_lot_patience, self.park_time_required, self.lot_visits))