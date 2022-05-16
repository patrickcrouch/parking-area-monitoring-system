from numpy import random
from itertools import cycle

class StudentCar(object):

    def __init__(self, env, student_car_label, parking_lots, pams_enabled):
        self.env = env
        # car label
        self.student_car_label = student_car_label
        # Max minutes to wait in a single lot with PAMS enabled
        if(pams_enabled == True):
            self.single_lot_patience = 0.1
        else:
            self.single_lot_patience = random.triangular(10.0, 15.0, 20.0)
        # Time needed in lot
        self.park_time_required = random.triangular(60.0, 180.0, 360.0)
        # randomized (but percentage weighted) parking lot preference selection
        self.lot_preference = []
        parking_lot_choice_probabilities = []
        for p_lot in parking_lots:
            parking_lot_choice_probabilities.append(p_lot.probability)
        self.lot_preference = random.choice(parking_lots, len(parking_lots), False, parking_lot_choice_probabilities)
        # Total wait time experienced
        self.wait_time = 0.0
        self.lot_visits = 0
        self.parked = False
        

    def park(self, env, student_car_data):
        # Get first lot preference
        arrival_time = env.now
        for lot in cycle(self.lot_preference):
            # start
            self.lot_visits += 1
            # break the loop and leave if total patience exceeded
            with lot.parking_spaces.request() as got_parking:
                parking_attempt = yield got_parking | env.timeout(self.single_lot_patience, 2)
                # Got a parking space
                if got_parking in parking_attempt:
                    self.wait_time = env.now - arrival_time
                    self.parked = True
                    student_car_data[self.student_car_label] = [self.wait_time, self.single_lot_patience, self.park_time_required, self.lot_visits, self.lot_preference]
                    yield env.timeout(self.park_time_required)
                    break
                elif 2 in parking_attempt.values():
                    self.parked = False
                    yield env.timeout(5.0)
                    continue
                else:
                    print('Something not caught: {}'.format(parking_attempt))
        # put excel line data for individual car stats here