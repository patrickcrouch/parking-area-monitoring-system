import simpy
import random
from objects.student_car import StudentCar
from objects.parking_lot import ParkingLot
from objects.scheduler import Scheduler

## Basic parameters

total_spaces = 4000
total_lots = 2
run_time = 600
num_cars = 0
max_wait = 0

## Tracking
wait_times = []

def setup(env):
    global num_cars
    global wait_times
    scheduler = Scheduler(1.0)
    parking_lots = []
    for lot_number in range(1,total_lots + 1):
        parking_lot = ParkingLot(env, total_spaces / total_lots, lot_number, 'Parking Lot %d' % lot_number)
        parking_lots.append(parking_lot)
    
    while True:
        num_cars += 1
        current_interarrival = scheduler.get(env.now)
        genexpo = random.expovariate(1.0 / current_interarrival)
        yield env.timeout(genexpo)
        car = StudentCar(env, '{}'.format(num_cars), parking_lots)
        env.process(car.park(env, wait_times))
        

env = simpy.Environment()
env.process(setup(env))
env.run(until = run_time)

avg_wait_time = sum(wait_times) / num_cars
max_wait = max(wait_times)

print('avg wait time was %d' % avg_wait_time)
print('max wait: {}'.format(max_wait))
print('num of cars was %d' % num_cars)