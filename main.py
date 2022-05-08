import simpy
import random
from objects.student_car import StudentCar
from objects.parking_lot import ParkingLot
from objects.scheduler import Scheduler

## Basic parameters

spaces_per_lot = 2000
total_lots = 2
run_time = 600
num_cars = 0
max_wait = 0

## Daily Tracking
wait_times = []
lots_visited = []
student_cars_parked = []

def setup(env):
    global num_cars
    global wait_times
    global lots_visited
    scheduler = Scheduler(100)
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
        

env = simpy.Environment()
env.process(setup(env))
env.run(until = run_time)

avg_wait_time = sum(wait_times) / num_cars
avg_lot_counts = sum(lots_visited) / num_cars
percent_successful_parks = sum(student_cars_parked) / num_cars
max_wait = max(wait_times)

print('avg wait time was %d' % avg_wait_time)
print('max wait: {}'.format(max_wait))
print('num of cars was %d' % num_cars)
print('avg num of lots visited by each car was {}'.format(avg_lot_counts))
print('percentage of successfully parked cars was {}'.format(percent_successful_parks * 100))