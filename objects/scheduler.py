class Scheduler(object):

    def __init__(self, busy_percentage = 1.0):
        self.hourly_arrival_rates = []
        # each value is 1 divided by cars per minute
        self.hourly_arrival_rates.append(1.0 / 2 / busy_percentage)
        self.hourly_arrival_rates.append(1.0 / 5 / busy_percentage)
        self.hourly_arrival_rates.append(1.0 / 10 / busy_percentage)
        self.hourly_arrival_rates.append(1.0 / 20 / busy_percentage)
        self.hourly_arrival_rates.append(1.0 / 30 / busy_percentage)
        reverse_arrivals = list(reversed(self.hourly_arrival_rates))
        for arrival in reverse_arrivals:
            self.hourly_arrival_rates.append(arrival)
    
    def get(self, current_time):
        interarrival_time = 0
        if current_time <= 60:
            interarrival_time = self.hourly_arrival_rates[0]
        elif current_time <= 120:
            interarrival_time = self.hourly_arrival_rates[1]
        elif current_time <= 180:
            interarrival_time = self.hourly_arrival_rates[2]
        elif current_time <= 240:
            interarrival_time = self.hourly_arrival_rates[3]
        elif current_time <= 300:
            interarrival_time = self.hourly_arrival_rates[4]
        elif current_time <= 360:
            interarrival_time = self.hourly_arrival_rates[5]
        elif current_time <= 420:
            interarrival_time = self.hourly_arrival_rates[6]
        elif current_time <= 480:
            interarrival_time = self.hourly_arrival_rates[7]
        elif current_time <= 540:
            interarrival_time = self.hourly_arrival_rates[8]
        elif current_time <= 600:
            interarrival_time = self.hourly_arrival_rates[9]
        return interarrival_time