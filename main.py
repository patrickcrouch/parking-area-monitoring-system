import simpy
from numpy import random
from objects.student_car import StudentCar
from objects.parking_lot import ParkingLot
from objects.scheduler import Scheduler
import xlsxwriter
from datetime import datetime

## Basic parameters
total_spaces = 3900
# Should be kept static for now
total_lots = 4
daily_run_time = 600
# Have to limit max cars to meet ANOVA requirements but
# unsure how to do this with varying exponential interarrivals
num_cars_max = 35200
num_cars = 0
max_wait = 0.0
# Number of weeks to run the simulation for and week's expected capacity percentage
runs_per_trial = 1
trial_data_map_list = [
    {'Trial Label': 1, 'Uniform Distribution': True, 'PAMS Enabled': False, 'Lots Evenly Sized': True},
    {'Trial Label': 2, 'Uniform Distribution': False, 'PAMS Enabled': False, 'Lots Evenly Sized': True},
    {'Trial Label': 3, 'Uniform Distribution': True, 'PAMS Enabled': True, 'Lots Evenly Sized': True},
    {'Trial Label': 4, 'Uniform Distribution': False, 'PAMS Enabled': True, 'Lots Evenly Sized': True},
    {'Trial Label': 5, 'Uniform Distribution': True, 'PAMS Enabled': False, 'Lots Evenly Sized': False},
    {'Trial Label': 6, 'Uniform Distribution': False, 'PAMS Enabled': False, 'Lots Evenly Sized': False},
    {'Trial Label': 7, 'Uniform Distribution': True, 'PAMS Enabled': True, 'Lots Evenly Sized': False},
    {'Trial Label': 8, 'Uniform Distribution': False, 'PAMS Enabled': True, 'Lots Evenly Sized': False}
]

# Traffic attenuation by weekday.  Subdued Monday start, midweek busy, Friday slowest.
weekday_scalars = [0.9, 0.95, 1.0, 0.95, 0.75]
activity_level = 100

## Per-vehicle Tracking
student_car_data = {}

## Spreadsheet output
workbook_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
workbook_name = 'PAMS_simulation_results_for_{}.xlsx'.format(workbook_date)
workbook = xlsxwriter.Workbook(workbook_name)

def setup(env, activity_level, is_uniform_distribution, pams_enabled, is_lots_evenly_sized, parking_lots):
    global num_cars
    global student_car_data
    scheduler = Scheduler(activity_level)
    first_choice_probability = []
    first_choice_probability.append(0.35)
    first_choice_probability.append(0.30)
    first_choice_probability.append(0.20)
    first_choice_probability.append(0.15)
    for lot_number in range(0,total_lots):
        if (is_lots_evenly_sized):
            spaces_per_lot = total_spaces / total_lots
        else:
            spaces_per_lot = (lot_number + 1) * 260
        parking_lot = ParkingLot(env, spaces_per_lot, lot_number + 1, 'Parking Lot {}'.format(lot_number + 1), first_choice_probability[lot_number])
        parking_lots.append(parking_lot)
    
    while num_cars < num_cars_max:
        if is_uniform_distribution:
            arrival_timeout = 3000.0 / num_cars_max
        else:
            interarrival = scheduler.get(env.now)
            arrival_timeout = random.exponential(interarrival)
        yield env.timeout(arrival_timeout)
        num_cars += 1
        car = StudentCar(env, '{}'.format(num_cars), parking_lots, pams_enabled)
        env.process(car.park(env, student_car_data))
    for lot in parking_lots:
        lot
        
## Kickoff!

for trial_data_map in trial_data_map_list:
    
    for run in range(0,runs_per_trial):
        # Setup individual worksheet for trial
        trial_run_label = 'Trial {} Run {}'.format(trial_data_map.get('Trial Label'), run + 1)
        workbook.add_worksheet('Summary of {}'.format(trial_run_label))
        is_uniform_distribution = trial_data_map.get('Uniform Distribution')
        is_pams_enabled = trial_data_map.get('PAMS Enabled')
        is_lots_evenly_sized = trial_data_map.get('Lots Evenly Sized')

        data_worksheet = workbook.add_worksheet(trial_run_label)
        data_worksheet.write(0, 0, 'Trial/Run')
        data_worksheet.write(0, 1, 'Uniform Arrival Distribution')
        data_worksheet.write(0, 2, 'PAMS System Enabled')
        data_worksheet.write(0, 3, 'Lots Evenly Sized')
        data_worksheet.write(1, 0, trial_run_label)
        data_worksheet.write(1, 1, is_uniform_distribution)
        data_worksheet.write(1, 2, is_pams_enabled)
        data_worksheet.write(1, 3, is_lots_evenly_sized)

        data_worksheet.write(2, 0, 'Car')
        data_worksheet.write(2, 1, 'Wait time (minutes)')
        data_worksheet.write(2, 2, 'Single lot max wait (minutes)')
        data_worksheet.write(2, 3, 'Park time (minutes)')
        data_worksheet.write(2, 4, 'Lots visited')

        parking_lot_1_data = []
        parking_lot_2_data = []
        parking_lot_3_data = []
        parking_lot_4_data = []

        for weekday in range(0,5):
            env = simpy.Environment()
            parking_lots = []
            env.process(setup(env, activity_level * weekday_scalars[weekday], is_uniform_distribution, is_pams_enabled, is_lots_evenly_sized, parking_lots))
            # env.run()
            env.run(until = daily_run_time)
            parking_lot_1_data.append(parking_lots[0])
            parking_lot_2_data.append(parking_lots[1])
            parking_lot_3_data.append(parking_lots[2])
            parking_lot_4_data.append(parking_lots[3])
            parking_lots.clear()

        # Output summary statistics per run
        max_wait = 0.0
        min_wait = 100.0
        total_wait = 0.0
        max_lot_patience = 0.0
        min_lot_patience = 100.0
        total_lot_patience = 0.0
        max_park_time = 0.0
        min_park_time = 100.0
        total_park_time = 0.0
        max_lot_visits = 0
        min_lot_visits = 25
        total_lot_visits = 0.0
        row_i = 3
        for key, value in student_car_data.items():
            data_worksheet.write(row_i, 0, key)
            for column in range(0, len(value) - 1):
                data_worksheet.write(row_i, column + 1, value[column])

            max_wait = max(max_wait, value[0])
            min_wait = min(min_wait, value[0])
            total_wait += value[0]
            max_lot_patience = max(max_lot_patience, value[1])
            min_lot_patience = min(min_lot_patience, value[1])
            total_lot_patience += value[1]
            max_park_time = max(max_park_time, value[2])
            min_park_time = min(min_park_time, value[2])
            total_park_time += value[2]
            max_lot_visits = max(max_lot_visits, value[3])
            min_lot_visits = min(min_lot_visits, value[3])
            total_lot_visits += value[3]
            row_i += 1
        
        avg_wait_time = total_wait / num_cars
        avg_lot_patience = total_lot_patience / num_cars
        avg_park_time = total_park_time / num_cars
        avg_lot_visits = total_lot_visits / num_cars

        summary_worksheet = workbook.get_worksheet_by_name('Summary of {}'.format(trial_run_label))
        summary_worksheet.write(0, 0, 'Summary Report')
        summary_worksheet.write(0, 1, workbook_date)
        summary_worksheet.write(2, 0, 'Number of Student Cars Out')
        summary_worksheet.write(2, 3, num_cars)
        summary_worksheet.write(4, 0, 'Student Cars (Entity)')
        summary_worksheet.write(4, 2, 'Average')
        summary_worksheet.write(4, 3, 'Maximum')
        summary_worksheet.write(4, 4, 'Minimum')
        summary_worksheet.write(4, 5, 'Total')
        summary_worksheet.write(5, 0, 'Wait Time (minutes)')
        summary_worksheet.write(5, 2, avg_wait_time)
        summary_worksheet.write(5, 3, max_wait)
        summary_worksheet.write(5, 4, min_wait)
        summary_worksheet.write(5, 5, total_wait)
        summary_worksheet.write(7, 0, 'Per-lot patience time (minutes)')
        summary_worksheet.write(7, 2, avg_lot_patience)
        summary_worksheet.write(7, 3, max_lot_patience)
        summary_worksheet.write(7, 4, min_lot_patience)
        summary_worksheet.write(7, 5, total_lot_patience)
        summary_worksheet.write(9, 0, 'Lot visits per car')
        summary_worksheet.write(9, 2, avg_lot_visits)
        summary_worksheet.write(9, 3, max_lot_visits)
        summary_worksheet.write(9, 4, min_lot_visits)
        summary_worksheet.write(9, 5, total_lot_visits)
        num_cars = 0
        
        
workbook.close()
