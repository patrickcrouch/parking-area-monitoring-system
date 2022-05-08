import simpy
import random

class StudentCar(object):

    def __init__(self, env, label, parking_lots):
        self.env = env
        # car label
        self.label = label
        self.parked = False
        # Max minutes to wait in a single lot
        self.single_lot_patience = random.triangular(7.0, 20.0, 13.0)
        # Max minutes to wait for space in entire sim
        lots_num = len(parking_lots)
        self.total_patience = random.triangular(7.0 * lots_num, 20.0 * lots_num, 12.0 * lots_num)
        # Time needed in lot
        self.park_time_required = random.triangular(60.0, 360.0, 180.0)
        # randomized lot preference order
        self.lot_preference = parking_lots.copy()
        random.shuffle(self.lot_preference)
        # How many lots student visited
        self.lot_count = 1
        # Total wait time experienced
        self.wait_time = 0
        

    def park(self, env, wait_times, lots_visited, student_cars_parked, lot_full_enabled=False):
        # Get first lot preference
        arrival_time = env.now
        for lot in self.lot_preference:
            # start
            # break the loop and leave if total patience exceeded
            if env.now - arrival_time > self.total_patience:
                self.parked = False
                print('Student car {} got frustrated and left'.format(self.label))
                break
            with lot.parking_spaces.request() as got_parking:
                parking_attempt = yield got_parking | env.timeout(self.single_lot_patience, 2)
                self.wait_time += env.now - arrival_time
                # Got a parking space
                if got_parking in parking_attempt:
                    self.parked = True
                    yield env.timeout(self.park_time_required)
                    break
                elif 2 in parking_attempt.values():
                    self.lot_count += 1
                    continue
                else:
                    print('Something not caught: {}'.format(parking_attempt))
        # put excel line data for individual car here
        wait_times.append(self.wait_time)
        lots_visited.append(self.lot_count)
        if self.parked == True:
            student_cars_parked.append(1.0)
        else:
            student_cars_parked.append(0.0)
            