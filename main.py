import simpy
import random
from objects.student_car import StudentCar
from objects.parking_lot import ParkingLot
from objects.scheduler import Scheduler

## Basic parameters

spaces_per_lot = 2000
total_lots = 2
daily_run_time = 600
num_cars = 0
max_wait = 0
# Number of weeks to run the simulation for and week's expected capacity percentage
week_data_map_list = [
    {'label': 'Week 01', 'capacity': 150},
    {'label': 'Week 02', 'capacity': 125},
    {'label': 'Week 03', 'capacity': 100},
    {'label': 'Week 04', 'capacity': 90},
    {'label': 'Week 05', 'capacity': 80},
    {'label': 'Week 06', 'capacity': 70},
    {'label': 'Week 07', 'capacity': 70},
    {'label': 'Week 08', 'capacity': 90},
    {'label': 'Week 09', 'capacity': 100},
    {'label': 'Week 10', 'capacity': 125}
]

# Traffic attenuation by weekday.  Subdued Monday start, midweek busy, Friday slowest.
weekday_scalars = [0.9, 0.95, 1.0, 0.95, 0.75]

## Daily Tracking
wait_times = []
lots_visited = []
student_cars_parked = []
reneges = []

def setup(env, capacity):
    global num_cars
    global wait_times
    global lots_visited
    global student_cars_parked
    scheduler = Scheduler(capacity)
    parking_lots = []
    for lot_number in range(1,total_lots + 1):
        parking_lot = ParkingLot(env, spaces_per_lot, lot_number, 'Parking Lot %d' % lot_number)
        parking_lots.append(parking_lot)
    
    while True:
        num_cars += 1
        current_interarrival = scheduler.get(env.now)
        genexpo = random.expovariate(1.0 / current_interarrival)
        yield env.timeout(genexpo)
        car = StudentCar(env, '{}'.format(num_cars), parking_lots)
        env.process(car.park(env, wait_times, lots_visited, student_cars_parked, False))
        
# Kickoff!
for week_data_map in week_data_map_list:
    week_label = week_data_map.get('label')
    week_capacity = week_data_map.get('capacity')
    for weekday in range(0,5):
        env = simpy.Environment()
        env.process(setup(env, week_capacity * weekday_scalars[weekday]))
        env.run(until = daily_run_time)

        avg_wait_time = sum(wait_times) / num_cars
        avg_lot_counts = sum(lots_visited) / num_cars
        percent_successful_parks = sum(student_cars_parked) / num_cars
        max_wait = max(wait_times)

        print('For {} day {}'.format(week_label, weekday + 1))
        print('avg wait time was %d' % avg_wait_time)
        print('max wait: {}'.format(max_wait))
        print('num of cars was %d' % num_cars)
        print('avg num of lots visited by each car was {}'.format(avg_lot_counts))
        print('percentage of successfully parked cars was {}'.format(percent_successful_parks * 100))
        print('Reneges: {}'.format(len(reneges)))

        # Clear everything after each run
        wait_times.clear()
        lots_visited.clear()
        student_cars_parked.clear()
        max_wait = 0
        num_cars = 0
        avg_wait_time = 0
        avg_lot_counts = 0