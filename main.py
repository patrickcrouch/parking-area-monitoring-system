import simpy
from numpy import random
from objects.student_car import StudentCar
from objects.parking_lot import ParkingLot
from objects.scheduler import Scheduler

## Basic parameters

spaces_per_lot = 975
total_lots = 4
daily_run_time = 600
num_cars = 0
max_wait = 0.0
# Number of weeks to run the simulation for and week's expected capacity percentage
week_data_map_list = [
    {'label': 'Week 01', 'capacity': 100} #,
    # {'label': 'Week 02', 'capacity': 125},
    # {'label': 'Week 03', 'capacity': 100},
    # {'label': 'Week 04', 'capacity': 90},
    # {'label': 'Week 05', 'capacity': 80},
    # {'label': 'Week 06', 'capacity': 70},
    # {'label': 'Week 07', 'capacity': 70},
    # {'label': 'Week 08', 'capacity': 90},
    # {'label': 'Week 09', 'capacity': 100},
    # {'label': 'Week 10', 'capacity': 125}
]

# Traffic attenuation by weekday.  Subdued Monday start, midweek busy, Friday slowest.
weekday_scalars = [0.9, 0.95, 1.0, 0.95, 0.75]


## Per-vehicle Tracking
student_car_data = {}

def setup(env, capacity):
    global num_cars
    global wait_times
    global student_car_data
    scheduler = Scheduler(capacity)
    parking_lots = []
    for lot_number in range(1,total_lots + 1):
        parking_lot = ParkingLot(env, spaces_per_lot, lot_number, 'Parking Lot %d' % lot_number)
        parking_lots.append(parking_lot)
    
    while True:
        num_cars += 1
        current_interarrival = scheduler.get(env.now)
        genexpo = random.exponential(current_interarrival)
        yield env.timeout(genexpo)
        car = StudentCar(env, '{}'.format(num_cars), parking_lots)
        env.process(car.park(env, student_car_data, False))
        
# Kickoff!
for week_data_map in week_data_map_list:
    week_label = week_data_map.get('label')
    week_capacity = week_data_map.get('capacity')
    for weekday in range(0,5):
        env = simpy.Environment()
        env.process(setup(env, week_capacity * weekday_scalars[weekday]))
        env.run(until = daily_run_time)

        max_wait = 0.0
        total_wait = 0.0
        max_lot_patience = 0.0
        total_lot_patience = 0.0
        max_park_time = 0.0
        total_park_time = 0.0
        max_lot_visits = 0
        total_lot_visits = 0.0
        for value in student_car_data.values():
            max_wait = max(max_wait, value[0])
            total_wait += value[0]
            max_lot_patience = max(max_lot_patience, value[1])
            total_lot_patience += value[1]
            max_park_time = max(max_park_time, value[2])
            total_park_time += value[2]
            max_lot_visits = max(max_lot_visits, value[4])
            total_lot_visits += value[4]

        avg_wait_time = total_wait / num_cars
        avg_lot_patience = total_lot_patience / num_cars
        avg_park_time = total_park_time / num_cars
        avg_lot_visits = total_lot_visits / num_cars
print("""Student car data:
number of cars: {} cars
max wait time: {} minutes
avg wait time: {} minutes
max_lot_patience: {} minutes
avg_lot_patience: {} minutes
max park time: {} minutes
avg_park_time: {} minutes
max lot visits: {} lots
avg lot visits: {} lots""".format(num_cars, max_wait, avg_wait_time, max_lot_patience, avg_lot_patience, max_park_time, avg_park_time, max_lot_visits, avg_lot_visits))
